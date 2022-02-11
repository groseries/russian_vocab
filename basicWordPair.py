import json
import reverso_api


class BasicWordPair:
    def __init__(self, vocab_word, english,no_translations=5,no_examples=2):
        self.vocab = vocab_word
        self.learn_box_trans = english
        self.lang = "ru"
        self.target = "en"
        self.ru_voice = "Alyona22k"
        self.arabic_voice = "Leila22k"
        self.number_of_different_translations = no_translations
        self.number_of_examples = no_examples
        self.reverso_context_client = reverso_api.context.ReversoContextAPI(source_text=self.vocab, source_lang=self.lang, target_lang=self.target)
        self.reverso_voice_client = reverso_api.voice.ReversoVoiceAPI()




    def get_deep_translate(self):
        _generator_of_trans_tuples = self.reverso_context_client.get_translations()
        self._list_of_trans_tuples = [next(_generator_of_trans_tuples) for _ in range(self.number_of_different_translations)]

    def get_examples(self):
        _generator_of_example_tuples = self.reverso_context_client.get_examples()
        self._list_of_example_tuples = [next(_generator_of_example_tuples) for _ in range(self.number_of_examples)]


    def get_voice(self):


class Vocab(BasicWordPair):



def parse(txt_file):
    with open(txt_file) as f:
        d = f.read()
    _list = d.split('\n')
    _list_of_pairs = [pair.split('/') for pair in _list]
    list_of_bwp = [BasicWordPair(pair[0], pair[1]) for pair in _list_of_pairs]
    list_of_bwp.pop(0)

    return list_of_bwp



