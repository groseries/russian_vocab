import reverso_api
from src.AnkiClient.AnkiClient import AnkiClient
from src.reverso_conjugator import ReversoConjugator
from src.reverso_conjugator import BasicConjugationForm


class Vocab:
    def __init__(self, vocab_word="привет", english="hi", no_translations=5, no_examples=2, deck="test_deck",
                 lang="ru"):
        self.__conjugation = None
        self.__part_of_speech = None
        self.list_of_example_tuples = None
        self.__html_conj_tables = None
        self.ankiclient = AnkiClient()

        self.vocab = vocab_word
        self.learn_box_trans = english
        self.deck_name = deck
        self.lang = lang
        if self.lang == "ru":
            self.language = "Russian"
        else:
            self.language = "Arabic"
        self.target = "en"
        self.ru_voice = "Alyona22k"
        self.arabic_voice = "Leila22k"
        self.number_of_different_translations = no_translations
        self.number_of_examples = no_examples
        self.reverso_context_client = reverso_api.context.ReversoContextAPI(source_text=self.vocab,
                                                                            source_lang=self.lang,
                                                                            target_lang=self.target)

        self.reverso_conjugate_client = ReversoConjugator.ReversoConjugator(source_text=self.vocab,
                                                                            source_lang=self.lang,
                                                                            target_lang=self.target)
        # self.reverso_voice_client = reverso_api.voice.ReversoVoiceAPI()

    def __update_data(self):
        self.__grammar = {"language": self.language,
                          "conjugation": self.__conjugation,
                          "part_of_speech": self.__part_of_speech,
                          "gender": "null",
                          "number": "null",
                          "aspect": "null",
                          "frequency": "null",
                          "case": "null",
                          "tense": "null"}

    @property
    def conjugation(self):
        return self.__grammar["conjugation"]

    @property
    def part_of_speech(self):
        return self.__grammar["part_of_speech"]

    @property
    def tense(self):
        return self.__grammar["tense"]

    @part_of_speech.setter
    def part_of_speech(self, value):
        assert isinstance(value, str), "part of speech must be string"
        self.__part_of_speech = value
        self.__update_data()

    @conjugation.setter
    def conjugation(self, value):
        assert isinstance(value, list), "conjugation is meant to be a list of various conjugation objects. Are you " \
                                        "using a list "
        for list in value:
            assert isinstance(list, BasicConjugationForm), "conjugtion is list of BasicConjugationForm Objects, " \
                                                           "ensure your list contains these objects "
        self.__conjugation = value
        self.__update_data()

    def get_deep_translate(self):
        _generator_of_trans_tuples = self.reverso_context_client.get_translations()
        self.list_of_trans_tuples = [next(_generator_of_trans_tuples) for _ in
                                     range(self.number_of_different_translations)]
        self.__grammar["part_of_speech"] = self.list_of_trans_tuples[0][3]
        self.__grammar["frequency"] = self.list_of_trans_tuples[0][2]

    def get_examples(self):
        _generator_of_example_tuples = self.reverso_context_client.get_examples()
        self.list_of_example_tuples = [next(_generator_of_example_tuples) for _ in range(self.number_of_examples)]

    def reverso_conjugate(self):
        self.reverso_conjugate_client.get_conjugations()

    def get_voice(self):
        pass

    def setup_note_model(self):
        """
            Creates a note model for the language if it isn't already created yet
        """
        r = self.ankiclient.get_model_names()
        if self.language + " Note" not in r:
            self.ankiclient.create_note_model(self.language)

    def find_notes(self):
        find = "findNotes"
        parameters = {"query": "deck:test_deck"}
        response = self.ankiclient._invoke(find, **parameters)
        return response

    def add_note(self):
        audio = [{
            "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
            "filename": "yomichan_ねこ_猫.mp3",
            "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            "fields": [
                self.language + " Audio"
            ]
        }, {
            "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
            "filename": "yomichan_ねこ_猫.mp3",
            "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            "fields": [
                "English Audio"
            ]
        }]
        tags = ["script_generated"]
        for key, value in self.__grammar.items():
            if value is not "null":
                tags.append(value)

        parameters = {"note": {
            "deckName": self.deck_name,
            "modelName": "Russian Test Note",
            "fields": {
                "English": self.learn_box_trans,
                self.language: self.vocab,
                "Gender": self.__grammar["gender"],
                "Aspect": self.__grammar["aspect"],
                "Case": self.__grammar["case"]
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
            "tags": tags,
            "audio": audio,
            "picture": [{
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                "filename": "black_cat.jpg",
                "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                "fields": [
                    "Conjugation"
                ]
            }]
        }
        }

        response = self.ankiclient._invoke("addNote", **parameters)
        return response


def parse(txt_file):
    """
        Parses Vocab from text file into a list of Vocab word objects
    :param txt_file: name of file to parse
    :return: list of Vocab word objs
    """
    with open(txt_file) as f:
        d = f.read()
    _list = d.split('\n')
    _list_of_pairs = [pair.split('/') for pair in _list]
    list_of_vocab = [Vocab(pair[0], pair[1]) for pair in _list_of_pairs]
    list_of_vocab.pop(0)

    return list_of_vocab
