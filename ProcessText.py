from sklearn import svm
import json
from Constants import stop_words, punctuations
from nltk.stem import PorterStemmer

class ProcessText:
    def __init__(self, file_path):
        self.stem_memo = dict()
        self.vocabulary = dict()
        self.identifier = 0
        self.tokenize_result = list()
        self.matrix = list()
        self.result = list()
        self.classifier = svm.SVC(kernel='linear', gamma='auto', C=2)

        self.read_input_file(file_path)
        self.train()

    def read_input_file(self, file_path):
        try:
            input_file = open(file_path, 'r')
        except FileNotFoundError:
            print('Could not open/find the file.')
        else:
            for row in input_file:
                json_row = json.loads(row)
                self.tokenize(json_row['reviewText'])
                self.result.append(int(json_row['overall']))

    def tokenize(self, string, predict=False):
        words, word, index = set(), list(), 0

        while True:
            if index == len(string) or string[index] == ' ':
                word = self.stem(''.join(word).strip())

                if len(word) > 0 and word not in stop_words():
                    words.add(word)

                    if word not in self.vocabulary:
                        self.vocabulary[word] = self.identifier
                        self.identifier += 1

                if index == len(string):
                    break

                word = list()
            elif string[index] not in punctuations():
                word.append(string[index].lower())

            index += 1

        if predict:
            return words

        self.tokenize_result.append(words)

    def stem(self, word):
        if word in self.stem_memo:
            return self.stem_memo[word]

        porter_stemmer = PorterStemmer()
        self.stem_memo[word] = porter_stemmer.stem(word)

        return self.stem_memo[word]

    def train(self):
        for row in self.tokenize_result:
            bag_of_words = [0] * len(self.vocabulary)

            for word in row:
                if word in self.vocabulary:
                    bag_of_words[self.vocabulary[word]] = 1

            self.matrix.append(bag_of_words)

        self.classifier.fit(self.matrix, self.result)

    def predict(self, string):
        row = self.tokenize(string, True)
        bag_of_words = [0] * len(self.vocabulary)

        for word in row:
            if word in self.vocabulary:
                bag_of_words[self.vocabulary[word]] = 1

        print(self.classifier.predict([bag_of_words]))

process_text = ProcessText('amazon_small.json')
process_text.predict('I hated how he kicks the ball.')



