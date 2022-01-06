import datetime
from datetime import date
from time import sleep

import httpx  # noqa
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from itou.job_applications.models import JobApplicationPoleEmploiNotificationLog
from itou.utils.apis.pole_emploi import (  # noqa
    POLE_EMPLOI_PASS_APPROVED,
    PoleEmploiIndividu,
    PoleEmploiMiseAJourPassIAEException,
    mise_a_jour_pass_iae,
)


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

    def get_maj_url(self):
        url = f"{settings.API_ESD_BASE_URL}/maj-pass-iae/v1/passIAE/miseAjour"
        if settings.API_ESD_MISE_A_JOUR_PASS_MODE != "production":
            # The test URL in recette, sandboxed mode
            url = f"{settings.API_ESD_BASE_URL}/testmaj-pass-iae/v1/passIAE/miseAjour"  # noqa
        return url

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
            print(f"encrypted_nir: {encrypted_nir}")
            # 3 requests/second max. I had timeout issues so 1 second takes some margins
            sleep(1)
        except Exception as e:
            print(e)
            return False

        DATE_FORMAT = "%Y-%m-%d"
        today = timezone.now().date()
        tomorrow = (timezone.now() + datetime.timedelta(days=1)).date()
        date_debut_pass = today.strftime(DATE_FORMAT)
        date_fin_pass = tomorrow.strftime(DATE_FORMAT)
        approval_number = "999992139048"
        siae_siret = "42373532300044"
        prescriber_siret = "36252187900034"
        params = {
            "idNational": encrypted_nir,
            "statutReponsePassIAE": POLE_EMPLOI_PASS_APPROVED,
            "typeSIAE": 837,
            "dateDebutPassIAE": date_debut_pass,
            "dateFinPassIAE": date_fin_pass,
            "numPassIAE": approval_number,
            "numSIRETsiae": siae_siret,
            "numSIRETprescripteur": prescriber_siret,
            "origineCandidature": "DEMA",
        }
        print(params)
        headers = {"Authorization": token, "Content-Type": "application/json"}  # noqa
        url = self.get_maj_url()  # noqa
        try:
            pass
            # r = httpx.post(url, json=params, headers=headers)
            # sleep(1)
            # print(r.content)
        except Exception as e:
            print(e)
            return False

        return True

    def handle(self, dry_run=False, **options):
        self.dump_settings()
        assert settings.API_ESD_MISE_A_JOUR_PASS_MODE == "sandbox"

        individuals = [
            PoleEmploiIndividu("LEILA", "HABTI", date(1977, 8, 14), "2770824520028"),
            PoleEmploiIndividu("DAVID", "PICCIN", date(1978, 3, 11), "1780347310022"),
        ]
        # Step 1: we get the API token
        try:
            token = JobApplicationPoleEmploiNotificationLog.get_token()
            sleep(1)
        except Exception as e:
            print(e)
            return False

        for individual in individuals:
            print(individual)
            self._notify_pole_employ(individual, token)
