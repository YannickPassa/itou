from dateutil.relativedelta import relativedelta

from django.test import TestCase

class ImportSiaeManagementCommandsTest(TestCase): 

    def test_get_creatable_conventions(self):
        # needs
        # Siaes wo conventions & source 'ASP'

        # if not in VUE_STRUCTURE_DF, siae.is_active must be False

        # if in VUE_STRUCTURE_DF
        # there must be no SiaeConvention objects for this asp_id and this kind

        # if does_siae_have_an_active_convention : check convention appended in list

        # if not does_siae_have_an_active_convention:
        # if siae_key not in INACTIVE_SIAE_LIST, check raise error
        # if siae_key in INACTIVE_SIAE_LIST, check convention_end_date
        # check convention appended in list



