

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import numpy as np
import pandas as pd
import gensim
import re

from gensim import parsing
import string
from nltk.tokenize import word_tokenize

table = str.maketrans('', '', string.punctuation)

file_to_read = "Questions.txt"  # file to be read
file_by_user = "queries.txt" # test file to be read
words_array = []  # array that takes in results of counts of two different sentences

doc = pd.read_csv(file_to_read, names=['questions'])
test_doc = pd.read_csv(file_by_user, names=['questions'])


# function that returns a bag of words and its length
def extract():
    # opening the training file and tokenizing
    with open(file_to_read, encoding="utf8") as file:
        text = file.read()
        tokens = word_tokenize(text)
        stripped = [w.translate(table) for w in tokens]
        words = sorted(set(re.split(r'\W+',
                                    text)))  # sorts, put into set, split into words and gets rid of punctuations and
        #  duplicates
        words = [word for word in stripped if word.isalpha()]
        words = [word.lower() for word in words]
        vocab_length = len(words)
        return words, vocab_length
    file.close()

# this function cleans the text provided, both training and testing data
def clean_text(textTest):
    wordset = set(stopwords.words('english'))  # remove stopwords
    textTest = textTest.lower()

    # Removing non-ASCII
    textTest = re.sub(r'[^\x00-\x7f]', r' ', textTest)

    # Removing whitespaces
    textTest = gensim.corpora.textcorpus.strip_multiple_whitespaces(textTest)

    # Removing stopwords
    stops = [word for word in textTest.split() if word not in wordset]

    # Preprocessed text after stop words removal
    textTest = " ".join(stops)

    # Removing punctuation marks
    textTest = gensim.parsing.preprocessing.strip_punctuation2(textTest)

    # Remove numerical numbers
    textTest = gensim.parsing.preprocessing.strip_numeric(textTest)

    return textTest


# executes the function of calculating the dot product and compares which is the most likely question and provide an
# answer
def executeFunction():
    test_x = test_doc['questions'].map(clean_text)
    words, vocab_length = extract()

    # read from file by user and tokenize
    with open(file_by_user, "r", encoding="utf8") as file:
        text = file.readlines()

        for i in text:
            result_array = []
            for y in words:
                if y in i:
                    result_array.append(1)
                else:
                    result_array.append(0)
            words_array.append(result_array)

        for i, j in zip(words_array, words_array[1:]):
            dot_product = np.dot(i, j)
            norm_i = np.linalg.norm(i)
            norm_j = np.linalg.norm(j)
            product_found = (dot_product / (norm_i * norm_j))

            # testing to see values being produced
            print(product_found)

    file.close()

# counts()
extract()
executeFunction()
