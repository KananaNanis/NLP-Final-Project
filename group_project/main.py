from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import re
from string import digits
import sys

"""
Implementation 1 Using A method similar to minimum edit distance
to determing similarities between sentence


"""


def clean_file(line):
    # Removing special unicode blocks from each line in the file
    result = re.sub(r"[�.]", "", line, flags=re.I)
    # Removing preceding digits
    result = result.lstrip(digits)
    # Removing unnecessary tab spaces from document
    result = result.strip()

    return result


def readFromQuestionsFile():
    questions_corpus = []

    # Reading from the question_file called Questions.txt
    question_file = open("Questions.txt", "r", encoding="utf8")

    # Appending the contents in the questions file into a question_corpus
    for line in question_file:
        result = clean_file(line)
        questions_corpus.append(result)

    return questions_corpus


#     Reading from the answer files called Answers.txt

def readFromAnswersFile():
    answers_corpus = []

    # Reading from the answers_file called Answers.txt
    answer_file = open("Answers.txt", "r", encoding="utf8")

    # Appending the contents in the questions file into a answers_corpus
    for line in answer_file:
        result = clean_file(line)
        answers_corpus.append(result)
    # print(answers_corpus)

    return answers_corpus


def readFromTopicsFile():
    topics_corpus = []

    # Reading from the answers_file called Answers.txt
    topics_file = open("Topics.txt", "r", encoding="utf8")

    # Appending the contents in the questions file into a answers_corpus
    for line in topics_file:
        result = clean_file(line)
        topics_corpus.append(result)
    # print(answers_corpus)

    return topics_corpus


# readFromFile()
def checkClosestDistance(line):
    # A list that contains the
    distance = []
    word = line

    question_corpus = readFromQuestionsFile()

    question_corpus.insert(0, word)

    # Vectorizer, reduces all sentences to it's cleanest form removing suffixes, Captials, punctuations etc
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(question_corpus).todense()
    # print(vectorizer.vocabulary_ , '\n')

    # comparing the features of the sentence with the features of all other sentences in the corpus
    for f in features:
        closest = euclidean_distances(features[0], f)
        distance.append(closest)

    # removing the initial sentence and answers generated to test the corpus
    question_corpus.pop(0)
    distance.pop(0)

    # The smallest distance means the closer the sentences are to each other
    minimum = min(distance)

    # Returning the index of our distance found
    index = distance.index(minimum)

    return index


# Function to determine the best answer per each sentence
def determineBestAnswer(sentence):
    answers_Corpus = readFromAnswersFile()
    index = checkClosestDistance(sentence)

    return answers_Corpus[index]


# Function for determining the best Topic
def determineBestTopic(sentence):
    topics_Corpus = readFromTopicsFile()
    index = checkClosestDistance(sentence)

    return topics_Corpus[index]


def testQnA(filename):
    testFile = open(filename, "r", encoding="utf8")

    # opening our results file
    resultsFile = open("qa_results.txt", "w")

    # writing answers to the results  file qa_results.txt
    for line in testFile:
        result = clean_file(line)
        answer = determineBestAnswer(result)
        resultsFile.write(answer + "\n")

    print("process completed and printed into qa_results.txt")
    resultsFile.close()


def testTM(filename):
    testFile = open(filename, "r", encoding="utf8")

    # creating the topics File
    resultsFile = open("topic_results.txt", "w")

    # Appending the answers generated the topics file into the results file
    for line in testFile:
        result = clean_file(line)
        topic = determineBestTopic(result)
        resultsFile.write(topic + "\n")

    print("process completed and printed into topics_results.txt")
    resultsFile.close()


if sys.argv[1] == "qa":
    test_file = sys.argv[2]
    print("\n")
    testQnA(test_file)

elif sys.argv[1] == "topic":
    test_file = sys.argv[2]
    print("\n")
    testTM(test_file)
