from django.test import TestCase
from django.core.management import call_command
from cvitae.settings import INSTALLED_APPS, BASE_DIR
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
import os

# Create your tests here.


class PrimaryTest(TestCase):

    def test_commands(self):
        call_command("loaddata", "--app=api", "--format=json", "demodump.json")

    def test_apps(self):
        if not "rest_framework" in INSTALLED_APPS:
            self.assertIsNone(
                None, "install rest_framework and add it to INSTALLED_APPS"
            )

    def test_api(self):
        client = APIClient()
        url = reverse("api-root")
        response = client.get(url)
        self.assertEqual(200, response.status_code)
        rj = response.json()
        routes = ["application", "admin", "template_config"]
        for i in routes:
            if not i in rj:
                self.assertIsNotNone(None, f"'{i}' is not included in routes")

    def test_templates(self):
        default_templates_path = os.path.join(BASE_DIR, "api/templates/versions")
        templates = [
            "body-default.html",
            "header-default.html",
        ].sort()
        for i in os.walk(default_templates_path):
            for ii in i[1]:
                path = os.path.join(default_templates_path, ii)
                for iii in os.walk(path):
                    self.assertEqual(iii[2].sort(), templates)
