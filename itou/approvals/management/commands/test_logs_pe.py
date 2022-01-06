from datetime import date
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from itou.job_applications.models import JobApplicationPoleEmploiNotificationLog
from itou.utils.apis.pole_emploi import mise_a_jour_pass_iae  # noqa
from itou.utils.apis.pole_emploi import PoleEmploiIndividu, PoleEmploiMiseAJourPassIAEException


class Command(BaseCommand):
    """
    Performs a sample HTTP request to pole emploi

    When ready:
        django-admin fetch_pole_emploi --verbosity=2
    """

    help = "Test synchronizing sample user data stored by Pole Emploi"

    # The following sample users are provided by Pole Emploi.
    # Dependending on their category, we know what kind of error the API should provide.

    API_DATE_FORMAT = "%Y-%m-%d"

    def dump_settings(self):
        print(f"API_ESD_AUTH_BASE_URL: {settings.API_ESD_AUTH_BASE_URL}")
        print(f"API_ESD_BASE_URL:      {settings.API_ESD_BASE_URL}")
        print(f"API_ESD_KEY:           {settings.API_ESD_KEY}")
        print(f"API_ESD_SECRET:        {settings.API_ESD_SECRET}")

    def _notify_pole_employ(self, individual: PoleEmploiIndividu, token: str) -> bool:
        if individual is None or not individual.is_valid():
            # We may not have a valid user (missing NIR, for instance),
            # in which case we can bypass this process entirely
            print("invalid")
            return False
        # Step 2 : we fetch the encrypted NIR
        try:
            encrypted_nir = JobApplicationPoleEmploiNotificationLog.get_encrypted_nir_from_individual(
                individual, token
            )
            print(encrypted_nir)
            # 3 requests/second max. I had timeout issues so 1 second takes some margins
            sleep(1)
        except PoleEmploiMiseAJourPassIAEException as e:
            print(e)
            return False
        # Step 3: we finally notify Pole Emploi that something happened for this user
        # try:
        #     mise_a_jour_pass_iae(self, mode, encrypted_nir, token)
        #     sleep(1)
        # except PoleEmploiMiseAJourPassIAEException as e:
        #     return False

        return True

    def handle(self, dry_run=False, **options):
        self.dump_settings()
        assert settings.API_ESD_MISE_A_JOUR_PASS_MODE == "sandbox"

        individuals = [
            PoleEmploiIndividu("LEILA", "HABTI", date(1977, 8, 14), "2770824520028"),
            PoleEmploiIndividu("David", "PICCIN", date(1978, 3, 11), "1780347310022"),
        ]
        # Step 1: we get the API token
        try:
            token = JobApplicationPoleEmploiNotificationLog.get_token()
            sleep(1)
        except Exception as e:
            print(e)
            return False

        for individual in individuals:
            self._notify_pole_employ(individual, token)
