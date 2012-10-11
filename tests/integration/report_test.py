# -*- coding: utf-8 -*-
from nav.tests.cases import ModPythonTestCase
from nav.models.profiles import Account, Organization, Location, Room
from django.db import transaction
from StringIO import StringIO

class ReportEncodingTest(ModPythonTestCase):

    def setUp(self):
        super(ReportEncodingTest, self).setUp()

        transaction.enter_transaction_management()
        transaction.managed(True)
        admin = Account.objects.get(login='admin')
        admin.name = u"ÆØÅ Test Administrator"
        admin.save()

        org = Organization(id=u"møøse", description=u"møøse biting unit")
        org.save()

        loc = Location(id=u"sømewhere", description="øver the rainbøw")
        loc.save()

        room = Room(id=u"æøå", description="The Norwegian blue room",
                    location=loc)
        room.save()


    def tearDown(self):
        super(ReportEncodingTest, self).tearDown()

        transaction.rollback()
        transaction.leave_transaction_management()


