#Russian_vocab
My library for automatically generating an Anki deck from a CSV.


### Features
1. Parses words to get vocabulary word's part of speed.
2. Fetches appropriate meta data for vocabulary word (noun-> declension, verb->conjugation)
3. Fetches text to speech file of vocabulary word
4. Fetches examples of word used in a sentence
5. Creates a new Anki note with all meta data
6. Study

### Usage (not implemented yet)
    from russian_vocab import parser
Store your csv as vocab.csv 

### Long term plans
Implement as a Flask/Twilio server that can just be texted to update my Anki decks automatically. 