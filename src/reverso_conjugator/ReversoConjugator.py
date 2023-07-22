import requests
import json
from jsonpointer import resolve_pointer
import pandas as pd
from .BasicConjugationForm import BasicConjugationForm
from collections import namedtuple

# ConjugationData = namedtuple("ConjugationData",("Unknown","Colloquial", "Fuzzy"))
# Conjugation = namedtuple("Conjugation",("Source", "Infinitive", "Participle", "Present", "Past", "Future", "ConjugationData"))
#
#
HEADERS = {"User-Agent": "Mozilla/5.0",
           "Content-Type": "application/json; charset=UTF-8"
           }


class ReversoConjugator:
    def __init__(self, source_text="читаешь", target_text="", source_lang="ru", target_lang="en"):
        self.__source_text, self.__target_text, self.__source_lang, self.__target_lang, self.__page_count = None, None, None, None, None
        self.source_text, self.target_text, self.source_lang, self.target_lang = source_text, target_text, source_lang, target_lang
        self.__update_data()

        self.base_url = "https://api-conjugator.reverso.net/api/conjugator/"

    def __update_data(self):
        self.__data = {
            "source_text": self.source_text,
            "target_text": self.target_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
        }
        self.__info_modified = True

    @property
    def source_text(self):
        return self.__source_text

    @property
    def target_text(self):
        return self.__target_text

    @property
    def source_lang(self):
        return self.__source_lang

    @property
    def target_lang(self):
        return self.__target_lang

    # TODO: Add verification that source text is a verb by making ReversoContext automatically call this for verbs

    @source_text.setter
    def source_text(self, value):
        assert isinstance(value, str), "source text must be a string"
        self.__source_text = value
        self.__update_data()

    @target_text.setter
    def target_text(self, value):
        assert isinstance(value, str), "target text must be a string"
        self.__target_text = value
        self.__update_data()

    @source_lang.setter
    def source_lang(self, value):
        assert isinstance(value, str), "language code must be a string"
        self.__source_lang = value
        self.__update_data()

    @target_lang.setter
    def target_lang(self, value):
        assert isinstance(value, str), "language code must be a string"
        self.__target_lang = value
        self.__update_data()

    def __repr__(self):
        return "Conjugator({source_text!r}, {target_text!r}, {source_lang!r}, {target_lang!r})" \
            .format(**self.__data)

    def __eq__(self, other):
        if isinstance(other, ReversoConjugator):
            return self.source_text == other.source_text \
                   and self.target_text == other.target_text \
                   and self.source_lang == other.source_lang \
                   and self.target_lang == other.target_lang
        return False

    def _extract_structured_conjugations(self, data):
        conj = {"infinitive_trans": resolve_pointer(data, "/Axis/0/Name"),
                "infinitive": resolve_pointer(data, "/Axis/0/Axis/0/Axis/0/Forms/0/Atoms/0/Value"),
                "form": resolve_pointer(data, "/Axis/1/Name"),  # Indicates indicative, subj, interr, conditional
                "present_trans": resolve_pointer(data, "/Axis/1/Axis/0/Name"),
                "present": BasicConjugationForm(json_data=resolve_pointer(data, "/Axis/1/Axis/0"), tense="present"),
                "past_trans": resolve_pointer(data, "/Axis/1/Axis/1/Name"),
                "past": BasicConjugationForm(json_data=resolve_pointer(data, "/Axis/1/Axis/1"), tense="past"),
                "future_trans": resolve_pointer(data, "/Axis/1/Axis/2/Name"),
                "future": BasicConjugationForm(json_data=resolve_pointer(data, "/Axis/1/Axis/2"), tense="future"),
                "imperative_trans": resolve_pointer(data, "/Axis/2/Name"),
                "imperative_s": resolve_pointer(data, "/Axis/2/Axis/0/Axis/0/Forms/0/Atoms/1/Value"),
                "imperative_pl": resolve_pointer(data, "/Axis/2/Axis/0/Axis/0/Forms/1/Atoms/1/Value"),
                }
        participles = {"participle_trans": resolve_pointer(data, "/Axis/3/Name"),
                       "active_participle_1": resolve_pointer(data, "/Axis/3/Axis/0/Axis/0/Forms/0/Atoms/0/Value"),
                       "active_participle_2": resolve_pointer(data, "/Axis/3/Axis/0/Axis/0/Forms/1/Atoms/0/Value"),
                       "passive_participle_1": resolve_pointer(data, "/Axis/3/Axis/1/Axis/0/Forms/1/Atoms/0/Value"),
                       "passive_participle_2": resolve_pointer(data, "/Axis/3/Axis/1/Axis/0/Forms/2/Atoms/0/Value")
                       }

        meta_data = {"IsFuzzy": data["IsFuzzyResult"],
                     "Colloquial": data["Colloquial"],
                     "ReflexiveForm": resolve_pointer(data, "/ReflexiveForm"),
                     "LinkedForm": resolve_pointer(data, "/LinkedForm"),
                     "LinkedFormType": resolve_pointer(data, "/LinkedFormType"),
                     "Alternatives": resolve_pointer(data, "/Alternatives"),
                     "OtherForms": resolve_pointer(data, "/OtherForms")
                     }
        return conj, participles, meta_data

    def get_conjugations(self):
        """Yields conjugation for the word (on the website you can find it just before the examples).

        Yields:
             Translation namedtuples.

        """
        endpoint = self.source_lang + "/" + self.source_text
        uri = self.base_url + endpoint
        response = requests.get(uri, headers=HEADERS)
        resp_dict = response.json()

        # with open("читаешь_response.json","w") as f:
        #     json.dump(response.json(),f)
        conjugation_json = self._extract_structured_conjugations(response.json())

        # for conj in conjugation_json:
        #     yield Conjugation(self.__data["source_text"], "Infinitive", "Participle", "Present", "Past", "Future", "ConjugationData")
