import json
import urllib.request


class AnkiClient:
    def __init__(self, port=8765):
        """
            Connects to Anki on local machine on provided port, allowing for various operations
        :param port:
        """
        self.port = str(port)

    @staticmethod
    def _request(action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def _invoke(self, action, **params):
        requestJson = json.dumps(self._request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    def get_model_names(self):
        params = {
            "action": "modelNames",
        }
        r = self._invoke(**params)
        return r

    def create_note_model(self, language):
        params= {
                "modelName": language+" Note",
                "inOrderFields": ["English", "English Audio", language, language+" Audio", "Gender", "Aspect", "Case",
                                  "Conjugation"],
                "css": "Optional CSS with default to builtin css",
                "isCloze": False,
                "cardTemplates": [
                    {
                        "Name": "Basic Vocab Pair",
                        "Front": "{{"+language+"}}",
                        "Back": "{{English}}"
                    }
                ]
            }

        r = self._invoke("createModel", **params)

    def sync(self):
        action = "sync"
        r = self._invoke(action)
