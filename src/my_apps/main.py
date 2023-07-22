from src.Vocab.Vocab import parse


def main():
    vocab_words = parse("../../text.txt")

    for word in vocab_words:
        word.get_deep_translate()
        if word.part_of_speech == "v":
            word.conjugate()
        word.get_voice()
        word.get_examples()
        word.add_note()



if __name__ == '__main__':

    main()


