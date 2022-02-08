from django.core.management.base import BaseCommand
from tqdm import tqdm

from itou.approvals.models import ApprovalsWrapper, PoleEmploiApproval


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

    def strategy_new_approval(self, approval, matching_approvals):
        # other option: we create another approval, based on the aggregate
        # data (but we have an issue of duplicate agrement number)
        # and we delete all the other. We can cheat somehow by using a suffix
        #
        if matching_approvals is not None and len(matching_approvals) > 0:
            approval = matching_approvals[0]
            pe_approval = PoleEmploiApproval(merged=True)

            pe_approval.pe_structure_code = approval.pe_structure_code
            pe_approval.number = approval.number[:12] + "dup"  # bypass duplicate number
            pe_approval.pole_emploi_id = approval.pole_emploi_id
            pe_approval.first_name = approval.first_name
            pe_approval.last_name = approval.last_name
            pe_approval.birth_name = approval.birth_name
            pe_approval.birthdate = approval.birthdate
            pe_approval.start_at = approval.start_at
            pe_approval.end_at = approval.end_at
            pe_approval.nir = approval.nir
            pe_approval.ntt_nia = approval.ntt_nia
            pe_approval.save()
            # we can delete all the initial approvals
            matching_approvals.delete()

    def strategy_keep_only_the_first(self, approval, matching_approvals):
        # Strategy:
        # - All the PoleEmploiApproval have their "merged" flag set to False initially
        # - We search for all the mergable approvals (merged=False, has a nir or an ntt/nia)
        # - For all those approvals, we:
        #     - search their duplicate: they share the same 12 digit "numero d’agrement".
        #     - We create and save a new unique approval, with the correct start/end date,
        #     and all the infos we have. This approval has the merged flag set to true
        #     - we delete the initial PoleEmploi Approvals #scream
        # - If an approval is alone, we simply set its merged flag to true

        # # print(approval.number)

        # for match in matching_approvals:
        #     print(f"\t{match.id} {match.number}, {match.first_name}, {match.birth_name}")
        # # according to ApprovalsWrapper.sort_approvals, "The first one is the longest and the most recent."
        matching_approvals = ApprovalsWrapper.sort_approvals(matching_approvals)
        matching_approvals[0].merged = True
        matching_approvals[0].save()
        # sadly, we can’t bulk delete anymore with the list so we have to create another queryset
        ids = [matching_approval.id for matching_approval in matching_approvals[1:]]
        PoleEmploiApproval.objects.filter(id__in=ids).delete()
        # for matching_approval in matching_approvals[1:]:
        #     matching_approval.delete()

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
