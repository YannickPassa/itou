# from dateutil.relativedelta import relativedelta
from django.test import TestCase

from itou.siaes.factories import SiaeFactory
from itou.siaes.management.commands._import_siae.convention import get_creatable_conventions
from itou.siaes.models import Siae, SiaeConvention


class ImportSiaeManagementCommandsTest(TestCase):
    def test_get_creatable_conventions(self):
        # active siae with active convention
        siae = SiaeFactory(source=Siae.SOURCE_ASP)
        self.assertTrue(siae.is_active)
        self.assertFalse(get_creatable_conventions())

        # active siae with unlinked convention
        siae = SiaeFactory(source=Siae.SOURCE_ASP)
        unlinked_convention = SiaeConvention.objects.get(id=siae.convention_id)
        unlinked_convention.siaes.clear()
        self.assertTrue(siae.is_active)
        self.assertTrue(SiaeConvention.objects.filter(asp_id=siae.asp_id, kind=siae.kind).exists())
        self.assertFalse(get_creatable_conventions())

        # inactive siae without convention
        siae = SiaeFactory(convention=None, source=Siae.SOURCE_ASP)
        self.assertFalse(siae.is_active)
        self.assertFalse(SiaeConvention.objects.filter(asp_id=siae.asp_id, kind=siae.kind).exists())

        # siae_without_convention_not_in_DF_inactive
        # siae_without_convention_not_in_DF_active

        # if not in VUE_STRUCTURE_DF, siae.is_active must be False

        # if in VUE_STRUCTURE_DF
        # there must be no SiaeConvention objects for this asp_id and this kind

        # if does_siae_have_an_active_convention : check convention appended in list

        # if not does_siae_have_an_active_convention:
        # if siae_key not in INACTIVE_SIAE_LIST, check raise error
        # if siae_key in INACTIVE_SIAE_LIST, check convention_end_date
        # check convention appended in list

        self.assertTrue(True)
