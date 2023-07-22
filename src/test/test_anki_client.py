import unittest


class TestAnkiClient(unittest.TestCase):
    def setUp(self) -> None:
        from src.AnkiClient.AnkiClient import AnkiClient
        self.client = AnkiClient()

    def test_request(self):
        my_action = "findNote"
        parameters = {"myparams": "myvals", "extra_key":"extra_val"}
        payload = self.client._request(my_action, **parameters)
        ideal = {'action': my_action, 'params': parameters, 'version': 6}
        self.assertEqual(ideal, payload)

    def test_invoke(self):
        my_action = "findNotes"
        parameters = {"query": "deck:test_deck"}
        r = self.client._invoke(my_action, **parameters)
        self.assertIn(1647210664049, r)

    def test_html_table_creation(self):
        my_action = "addNote"
        with open("table_test.html") as f:
            s = f.read()
        parameters = {"note": {
            "deckName": "test_deck",
            "modelName": "Russian Test Note",
            "fields": {
                "English": s,
                "Gender": "null",
                "Aspect": "null",
                "Case": "null"
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "null",
                "duplicateScopeOptions": {
                    "deckName": "null",
                    "checkChildren": True,
                    "checkAllModels": True
                }
            },
        }
        }
        r = self.client._invoke(my_action, **parameters)

    def test_create_note_model(self):
       with self.assertRaises(Exception) :
           self.client.create_note_model("Russian")

    def test_get_model_names(self):
        r = self.client.get_model_names()
        self.assertIn("Russian Note", r)

    def test_sync(self):
        r = self.client.sync()
        self.assertIsNone(r)

if __name__ == '__main__':
    unittest.main()
