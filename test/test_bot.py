import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bot')))
from main import Uptime_start

class TestChecker(unittest.TestCase):
    def test_valid_url(self):
        self.assertTrue(get_web("https://google.com"))

    def test_invalid_url(self):
        self.assertFalse(get_web("http://thisurldoesnotexist1234.com"))

if __name__ == "__main__":
    unittest.main()