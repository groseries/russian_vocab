import unittest
from src.reverso_conjugator.ReversoConjugator import ReversoConjugator


class TestReversoConjugator(unittest.TestCase):
    def setUp(self) -> None:
        self.client = ReversoConjugator(source_text="شرب", source_lang="ar")

    def test_get_conjugations(self):
        self.client.get_conjugations()

    def test_extract_structured_conjugations_ru(self):
        """
            Verify that it can do a basic distillation of a russian response
            Specifically: separate out the meta data from the conjugations
        """

    def test_extract_structured_conjugations_ar(self):
        """
            Verify that it can do a basic distillation of a russian response
            Specifically: separate out the meta data from the conjugations
        """

    def test_extract_structured_conjugations_es(self):
        """
            Test general case
        """


if __name__ == '__main__':
    unittest.main()
