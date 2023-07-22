import json
from jsonpointer import resolve_pointer


class BasicConjugationForm:
    def __init__(self, json_data, tense):
        self.tense = tense
        self.foreign_lang_tense = resolve_pointer(json_data, "/Name")
        self.number_of_forms = len(resolve_pointer(json_data, "/Axis/0/Forms"))

        self.basic_forms = {}
        self.__import_arbitrary_num_forms(unresolved_dict=json_data)

        # if self.number_of_forms == 6:
        #     self.__import_6_person_forms(json_data)
        # elif self.number_of_forms == 4:

    def __import_6_person_forms(self, unresolved_dict):
        self.basic_forms = {"1s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/0/Atoms/1/Value"),
                            "2s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/1/Atoms/1/Value"),
                            "3s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/2/Atoms/1/Value"),
                            "1pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/3/Atoms/1/Value"),
                            "2pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/4/Atoms/1/Value"),
                            "3pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/5/Atoms/1/Value"),
                            }
        self.pronouns = {"1s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/0/Atoms/0/Value"),
                         "2s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/1/Atoms/0/Value"),
                         "3s": resolve_pointer(unresolved_dict, "/Axis/0/Forms/2/Atoms/0/Value"),
                         "1pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/3/Atoms/0/Value"),
                         "2pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/4/Atoms/0/Value"),
                         "3pl": resolve_pointer(unresolved_dict, "/Axis/0/Forms/5/Atoms/0/Value"),
                         }

    def __import_4_person_forms(self, unresolved_dict):
        """
        #TODO: additional scraping to do
        :param unresolved_dict:
        :return:
        """
        pass

    def __import_arbitrary_num_forms(self, unresolved_dict):
        for i in range(0, self.number_of_forms):
            pronoun_pointer = "/Axis/0/Forms/"+str(i)+"/Atoms/0/Value"
            verb_pointer = "/Axis/0/Forms/"+str(i)+"/Atoms/1/Value"
            pronoun = resolve_pointer(unresolved_dict, pronoun_pointer)
            verb = resolve_pointer(unresolved_dict, verb_pointer)
            self.basic_forms.update({pronoun:verb})

    def __future_depth(self,unresolved_dict):
        """#TODO: Implement in the future (lol)"""
        pass
