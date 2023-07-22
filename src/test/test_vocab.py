import unittest


class VocabTest(unittest.TestCase):
    def setUp(self) -> None:
        from src.Vocab.Vocab import Vocab
        self.words = Vocab()

    def test_deep_translate(self):
        self.words.get_deep_translate()
        self.assertEqual(self.words.list_of_trans_tuples[0][0], "привет")

    def test_get_examples(self):
        self.words.get_examples()
        self.assertEqual(self.words.list_of_example_tuples[0][0][0], "Марко сказал передать вам особый привет.")

    def test_find_notes(self):
        r = self.words.find_notes()
        self.assertIn(1644636739131, r)

    def test_add_note(self):
        r = self.words.add_note()
        print(r)
        r_find = self.words.find_notes()
        self.assertIn(r, r_find)



if __name__ == '__main__':
    unittest.main()
