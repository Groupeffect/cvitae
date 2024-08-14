from django.test import TestCase

# Create your tests here.


class PrimaryTest(TestCase):

    def test_load(self):
        self.assertIsNone(None)
    
    def test_dump(self):
        self.assertEqual(True,False)