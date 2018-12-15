##import libraries
import sys
import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer


##read the Questions and Topics datasets
def readData():
    get_qtns = pd.read_csv('Questions.txt', names=['questions'], index_col= None)
    get_topics = pd.read_csv('Topics.txt', names=['topics'],index_col= None)
    # concatenate questions and topics
    data = pd.concat([get_qtns, get_topics], axis=1)
    # put questions and topics in a list
    qtns=data.questions.values.tolist()
    topics=data.topics.values.tolist()
    return qtns, topics
##    print(qtns)

##read_files()

#lemmatization on questions using WordNetLemmatizer model 
def lemmatization(qtns):
    lemmed_qtns = []
    wnl = WordNetLemmatizer()
    for qtn in qtns:
        lemmed_qtns.append(' '.join(wnl.lemmatize(token)for token in nltk.word_tokenize(qtn)))
    return (lemmed_qtns)

# stemming on questions using LancasterStemmer model
def do_stemming(qtns):
    stemmed_qtns = []
    ls = LancasterStemmer()
    for qtn in qtns:
        stemmed_qtns.append(' '.join(ls.stem(token)for token in nltk.word_tokenize(qtn)))
    return(stemmed_qtns)

#training the dataset
def train(qtns, features):
    # initialize CountVectorizer to extract word features with normalization
    count_vect = CountVectorizer(stop_words='english',lowercase = True, ngram_range = (1,1), max_df = 0.5, min_df = 1)
    # solve frequency discrepancies among long and short sentences
    tf_transform = TfidfTransformer()
    X_train_ = count_vect.fit_transform(r for r in qtns)
    X_train_tf = tf_transform.fit_transform(X_train_)

    # splitting data into test and training set
    X_train, X_test, Y_train, Y_test = train_test_split(X_train_tf, features, random_state=35, train_size=0.70, test_size=0.30)

    # training the classifier
    LR = LogisticRegression(solver='lbfgs')
    LR_Model=LR.fit(X_train, Y_train)    
    # return trained model
    return LR,tf_transform, count_vect, LR_Model, X_test, Y_test

## testing the dataset
def test(filename, questions, labels,writeFile="topic_results.txt"):
    LR, tf_transform, count_vect, LR_Model, X_test, Y_test = train(
        questions, labels)
    test_data = []
    with open(filename, 'r') as rf:
        for line in rf:
            test_data.append(line.strip('\r\n'))
    X_test_features = count_vect.transform(test_data) 
    X_test_tf = tf_transform.transform(X_test_features)
    # predict test sentences
    predicted = LR.predict(X_test_tf)
    # write to file
    with open(writeFile, 'w') as wf:
        for prediction in predicted:
            wf.write(str(prediction) + '\n')
    predicted = LR_Model.predict(X_test)
    print("Accuracy: ",round(accuracy_score(Y_test, predicted)*100),4)
    return (predicted, "\n")

def initialize_functions():
    qtns, topics = readData()
    qtns2 = lemmatization(qtns)
    qtns3 = do_stemming(qtns2)
    test('Testers.txt', qtns3, topics)

if __name__ == '__main__':
    initialize_functions()

