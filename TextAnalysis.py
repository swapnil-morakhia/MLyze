from textblob import TextBlob

class TextAnalysis:
    def __init__(self, string):
        self.result = TextBlob(string)
        self.dictionary_response = {'sentences': dict(), 'nouns': set()}

        self.add_sentiments()
        self.add_nouns()

    def get_response(self):
        return self.dictionary_response

    def add_sentiments(self):
        sentences = self.result.sentences

        for sentence in sentences:
            self.dictionary_response['sentences'][sentence.string] = sentence.sentiment.polarity

    def add_nouns(self):
        for noun in self.result.noun_phrases:
            self.dictionary_response['nouns'].add(noun)

ta = TextAnalysis('i love it. i loath it. it is terrible.')
