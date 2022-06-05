import re

from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
file = open("Document.txt")

line = file.read().replace("\n", " ")
file.close()

training_doc1 = """
how are glacier caves formed ?	A partly submerged glacier cave on Perito Moreno Glacier .	0
how are glacier caves formed ?	The ice facade is approximately 60 m high	0
how are glacier caves formed ?	Ice formations in the Titlis glacier cave	0
how are glacier caves formed ?	A glacier cave is a cave formed within the ice of a glacier .	1
how are glacier caves formed ?	Glacier caves are often called ice caves , but this term is properly used to describe bedrock caves that contain year-round ice .	0
How are the directions of the velocity and force vectors related in a circular motion	In physics , circular motion is a movement of an object along the circumference of a circle or rotation along a circular path .	0
How are the directions of the velocity and force vectors related in a circular motion	It can be uniform , with constant angular rate of rotation ( and constant speed ) , or non-uniform with a changing rate of rotation .	0
How are the directions of the velocity and force vectors related in a circular motion	The rotation around a fixed axis of a three-dimensional body involves circular motion of its parts .	0
How are the directions of the velocity and force vectors related in a circular motion	The equations of motion describe the movement of the center of mass of a body .	0
"""


class MarkovChain:
    def __init__(self):
        self.lookup_dict = defaultdict(list)

    def add_document(self, string):
        preprocessed_list = self._preprocess(string)
        pairs = self.__generate_tuple_keys(preprocessed_list)
        for pair in pairs:
            self.lookup_dict[pair[0]].append(pair[1])
        pairs2 = self.__generate_2tuple_keys(preprocessed_list)
        for pair in pairs2:
            self.lookup_dict[tuple([pair[0], pair[1]])].append(pair[2])
        pairs3 = self.__generate_3tuple_keys(preprocessed_list)
        for pair in pairs3:
            self.lookup_dict[tuple([pair[0], pair[1], pair[2]])].append(pair[3])

    def _preprocess(self, string):
        cleaned = re.sub(r'\W+', ' ', string).lower()
        tokenized = word_tokenize(cleaned)
        return tokenized

    def __generate_tuple_keys(self, data):
        if len(data) < 1:
            return

        for i in range(len(data) - 1):
            yield [data[i], data[i + 1]]

    def __generate_2tuple_keys(self, data):
        if len(data) < 2:
            return

        for i in range(len(data) - 2):
            yield [data[i], data[i + 1], data[i + 2]]


    def __generate_3tuple_keys(self, data):
         if len(data) < 3:
            return

         for i in range(len(data) - 3):
          yield [data[i], data[i + 1], data[i + 2], data[i + 3]]


    def oneword(self, string):
      return Counter(self.lookup_dict[string]).most_common()[:3]


    def twowords(self, string):
         suggest = Counter(self.lookup_dict[tuple(string)]).most_common()[:3]
         if len(suggest) == 0:
              return self.oneword(string[-1])
         return suggest


    def threewords(self, string):
         suggest = Counter(self.lookup_dict[tuple(string)]).most_common()[:3]
         if len(suggest) == 0:
             return self.twowords(string[-2:])
         return suggest


    def morewords(self, string):
      return self.threewords(string[-3:])


    def generate_text(self, string):
         if len(self.lookup_dict) > 0:
             tokens = string.split(" ")
         if len(tokens) == 1:
            print("Next word suggestions:", self.oneword(string))
         elif len(tokens) == 2:
            print("Next word suggestions:", self.twowords(string.split(" ")))
         elif len(tokens) == 3:
            print("Next word suggestions:", self.threewords(string.split(" ")))
         elif len(tokens) > 3:
            print("Next word suggestions:", self.morewords(string.split(" ")))
         return

'''
my_markov = MarkovChain()
my_markov.add_document(training_doc1)
my_markov.generate_text(input().lower())
'''
my_markov = MarkovChain()
my_markov.add_document(line)
my_markov.generate_text(input().lower())