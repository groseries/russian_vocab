import json
import unittest
from src.reverso_conjugator import BasicConjugationForm


class TestBasicConjugationForm(unittest.TestCase):
    def setUp(self) -> None:
        with open("conjugation_test.json") as f:
            self.json_data = json.load(f)

    def test_parsing(self):
        conjugation = BasicConjugationForm(self.json_data, "present")
        self.assertIsInstance(conjugation, BasicConjugationForm)
        # add assertion here


if __name__ == '__main__':
    unittest.main()
