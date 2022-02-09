from django.core.management.base import BaseCommand
from tqdm import tqdm

from itou.approvals.models import PoleEmploiApproval


class Command(BaseCommand):
    """
    ./manage.py update_nir_from_pe_data --file-path="./imports/LISTE_IAE_NIR_PNI-pruned-from-fluff.csv" --dry-run

    Ajoute le NIR ou le NIA/NTT dans les objets PoleEmploiApproval à partir de l’export LISTE_IAE_NIR_PNI.
    Croise les infos à partir du numéro de pass
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", dest="dry_run", action="store_true", help="Only print possible errors and stats"
        )

    def create_new_merged_approval(self, approval, matching_approvals):
        # we create another approval, based on the aggregate
        # data (but we have an issue of duplicate agrement number)
        # and we delete all the other. We can cheat somehow by using a suffix,
        # that will be discarded once all the single PEApprovals are merged
        #
        if matching_approvals is not None and len(matching_approvals) > 0:
            approval = matching_approvals[0]
            pe_approval = PoleEmploiApproval(merged=True)
            # First, we need to find the exact duration:
            # - the oldest start date
            # - the most recent end date
            # - if we have a suspension during covid lockdown, we need to add 3 months
            start_date = min([a.start_date for a in matching_approvals])
            end_date = max([a.end_date for a in matching_approvals])
            if pe_approval.overlaps_covid_lockdown():
                pe_approval.end_at = pe_approval.get_extended_covid_end_at()

            # Then, we need to create a valid, non-existing approval number.
            # We’ll remove the "dup" suffix in a later step
            pe_approval.number = approval.number[:12] + "dup"  # bypass duplicate number

            # Finally, we can copy all the other data we have
            pe_approval.pe_structure_code = approval.pe_structure_code
            pe_approval.pole_emploi_id = approval.pole_emploi_id
            pe_approval.first_name = approval.first_name
            pe_approval.last_name = approval.last_name
            pe_approval.birth_name = approval.birth_name
            pe_approval.birthdate = approval.birthdate
            pe_approval.start_at = start_date
            pe_approval.end_at = end_date
            pe_approval.nir = approval.nir
            pe_approval.ntt_nia = approval.ntt_nia

            pe_approval.save()
            # we can bulk-delete all the initial approvals
            matching_approvals.delete()

    def handle(self, dry_run=False, **options):
        self.dry_run = dry_run
        self.stdout.write("Merging approvals / PASS IAE")

        pe_approvals = PoleEmploiApproval.objects.with_nir_ntt_or_nia().filter(merged=False)
        pbar = tqdm(total=len(pe_approvals))
        for approval in pe_approvals[:1000]:
            matching_approvals = PoleEmploiApproval.objects.filter(number__startswith=approval.number[:12])  # noqa
            self.strategy_keep_only_the_first(approval, matching_approvals)

            pbar.update(1)
        pbar.close()
