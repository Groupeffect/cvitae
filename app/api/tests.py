from django.test import TestCase
from django.core.management import call_command
from cvitae.settings import INSTALLED_APPS
# Create your tests here.


class PrimaryTest(TestCase):

    def test_apps(self):
        if not "rest_framework" in INSTALLED_APPS:
            self.assertIsNone(None, "install rest_framework and add it to INSTALLED_APPS")
    
    def test_commands(self):
        call_command("loaddata", "--app=api", "--format=json", "demodump.json")

        