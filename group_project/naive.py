
# using Naive Bayes classifier for Topic Modelling
# importing libraries
import nltk                      
import pandas as pd              
import re                         
from nltk.corpus import stopwords  
from gensim import parsing       
import gensim
import numpy as np

# Loading in the training data with Pandas
doc = pd.read_csv("./mergedfile.txt")

## Collect all unique author names from author column
topic_names = doc['Topic'].unique()
topic_to_id = {}
assign_id = 0
for name in topic_names:
    topic_to_id[name] = assign_id
    assign_id += 1  ## Get a new id for new author
id_to_topic = {v: k for k, v in topic_to_id.items()}

## Add a new column to pandas dataframe, with the author name mapping
def get_topic_id(topic_name):
    return topic_to_id[topic_name]

doc['topic_id'] = doc['Topic'].map(get_topic_id)

doc.head()

def transformText(text):
    
    stops = set(stopwords.words("english"))
    
    # Convert text to lower
    text = text.lower()
    # Removing non ASCII chars    
    text = re.sub(r'[^\x00-\x7f]',r' ',text)
    
    # Removing all the stopwords
    filtered_words = [word for word in text.split() if word not in stops]

    text = gensim.parsing.preprocessing.strip_numeric(text)
    
    
    # Stemming
    return gensim.parsing.preprocessing.stem_text(text)


doc['Question'] = doc['Question'].map(transformText)


## Split the data 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(doc['Question'], doc['topic_id'], 
                                                    test_size=0.33, random_state=42)
#building the model
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
X_train_counts.shape

## Get the TF-IDF vector representation of the data
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, y_train)

## Prediction 

X_new_counts = count_vect.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
counter  = 0
for doc, category in zip(X_test, predicted):
    print('%r => %s' % (doc, id_to_topic[category]))
    if(counter == 10):
        break
    counter += 1    
acc=np.mean(predicted == y_test)
print(acc)






