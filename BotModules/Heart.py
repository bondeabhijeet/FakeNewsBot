import requests
import time
from bs4 import BeautifulSoup
from telegram.parsemode import ParseMode
from BotModules import SendMessage as SendMessage

# Importing 

from nltk import stem
import numpy as np                                                          # Useful for making numpy arrays
import pandas as pd                                                         # Useful for creating the dataframe and storing the data in dataframe 
import re                                                                   # Regular expression (usefull for searching the text in a document)
from nltk.corpus import stopwords                                           # The words the dont add much value to our text
from nltk.stem.porter import PorterStemmer                                  # This gives the root word for a particular word.
from sklearn.feature_extraction.text import TfidfVectorizer                 # To convert text into feature vectors (ie. numbers)
from sklearn.model_selection import train_test_split                        # This helps us to seperate training data and testing data
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import RandomForestClassifier

class News():
    def __init__(self):
        self.news_dataset = pd.read_csv('BotModules/train.csv')
        nltk.download('stopwords')
        print('\n[&] : Shape: ', self.news_dataset.shape)
        print('\n[&] : The Data Set looks like:\n', self.news_dataset.head())
        print('\n[&] : DataSet Stats:\n', self.news_dataset.isnull().sum() )
        self.news_dataset = self.news_dataset.fillna('')
        print('\n[&] : New Stats:\n', self.news_dataset.isnull().sum())
        self.news_dataset['content'] = self.news_dataset['author'] + ' ' + self.news_dataset['title']
        X = self.news_dataset.drop('label', axis=1)                                  
        Y = self.news_dataset['label']
        self.port_stem = PorterStemmer()

        # def stemming(content):
        #     stemmed_content = re.sub('[^a-zA-Z]', ' ', content)                 # using regular expression selecting only the a-z & A-Z set and replacing other things with ' ' from content. If number or comma or other things are found then it will be replaced with ' '.
        #     stemmed_content = stemmed_content.lower()                           # Converting all the letters into lower case letters
        #     stemmed_content = stemmed_content.split()                           # Converting all the all the content into list
            
        #     stemmed_content = [self.port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')] # Selecting the words which arent there in stopwords and performing the stem operation.
        #     stemmed_content = ' '.join(stemmed_content)                         # Joining the words to again make a sentence.
        #     return stemmed_content

        self.news_dataset['content'] = self.news_dataset['content'].apply(self.stemming)
        print('\n[&] : Stemmed Dataset:\n', self.news_dataset['content'])
        self.X = self.news_dataset['content'].values    # Independent var

        self.Y = self.news_dataset['label'].values      # Dependent Var

        print('\n[&] : X:\n', self.X)
        print('\n[&] : Y:\n', self.Y)

        self.vectorizer = TfidfVectorizer()                                          # Tf : term frequency (ie. counts the number of times a word is repeating in a document and so it understands that a word is important and assigns it a value) and idf: inverse document frequency (Detects the words which are repeating and dont have significant value and assigns it a lesser important values (Avengers))
        self.vectorizer.fit(self.X)                                                       # Fitting the X to vectorizer function

        self.X = self.vectorizer.transform(self.X)
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.2, stratify=self.Y, random_state=2)

        ############################################################################## LOGISTIC REGRESSION

        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.Y_train)

        self.X_train_prediction = self.model.predict(self.X_train)                             # Predicting the accuracy on X_train data and store the labels in X_train_prediction
        self.training_data_accuracy = accuracy_score(self.X_train_prediction, self.Y_train)

        print('Accuracy score of the training data:', self.training_data_accuracy)

        # accuracy score on the training data

        self.X_test_prediction = self.model.predict(self.X_test)                               # Predicting the accuracy on X_train data and store the labels in X_train_prediction
        self.test_data_accuracy = accuracy_score(self.X_test_prediction, self.Y_test)          # Comparing our predicted data with the actual labels (from dataset)

        print('Accuracy score of the testing data:', self.test_data_accuracy)

        ############################################################################## RANDOM FOREST CLASSIFIER

        self.clf = KNeighborsClassifier(n_neighbors=3)
        self.clf.fit(self.X_train, self.Y_train)

        self.X_train_prediction = self.clf.predict(self.X_train)                               # Predicting the accuracy on X_train data and store the labels in X_train_prediction
        self.training_data_accuracy = accuracy_score(self.X_train_prediction, self.Y_train)    # Comparing our predicted data with the actual labels (from dataset)

        print('Accuracy score of the training data:', self.training_data_accuracy)

        # accuracy score on the training data

        self.X_test_prediction = self.clf.predict(self.X_test)                                 # Predicting the accuracy on X_train data and store the labels in X_train_prediction
        self.test_data_accuracy_CLF = accuracy_score(self.X_test_prediction, self.Y_test)          # Comparing our predicted data with the actual labels (from dataset)

        print('Accuracy score of the testing data:', self.test_data_accuracy_CLF)
    
    def stemming(self, content):
            stemmed_content = re.sub('[^a-zA-Z]', ' ', content)                 # using regular expression selecting only the a-z & A-Z set and replacing other things with ' ' from content. If number or comma or other things are found then it will be replaced with ' '.
            stemmed_content = stemmed_content.lower()                           # Converting all the letters into lower case letters
            stemmed_content = stemmed_content.split()                           # Converting all the all the content into list
            
            stemmed_content = [self.port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')] # Selecting the words which arent there in stopwords and performing the stem operation.
            stemmed_content = ' '.join(stemmed_content)                         # Joining the words to again make a sentence.
            return stemmed_content


    def LGR(self, CommandToReplace, RecievedMsg, context, update, MessageID):
        
        q = list()
        query = ValidQuery(RecievedMsg, CommandToReplace, context)

        query = self.stemming(query)

        q.append(query)

        vectorizer = TfidfVectorizer()                                          # Tf : term frequency (ie. counts the number of times a word is repeating in a document and so it understands that a word is important and assigns it a value) and idf: inverse document frequency (Detects the words which are repeating and dont have significant value and assigns it a lesser important values (Avengers))
        vectorizer.fit(q)                                                       # Fitting the X to vectorizer function

        q = self.vectorizer.transform(q)
        X_news = q

        prediction = self.model.predict(X_news)

        print(prediction)

        if prediction[0] == 0:
            SendMessage.SendMessage(update, context, f"News status : <code>REAL</code> \nEngine : <code>LOGISTICREGRESSION</code> \nTest model accuracy : <code>{self.test_data_accuracy}</code>", MessageID)
            print('[ LGR ] : The news is real')
        else:
            SendMessage.SendMessage(update, context, f"News status : <code>FAKE</code> \nEngine : <code>LOGISTICREGRESSION</code> \nTest model accuracy : <code>{self.test_data_accuracy}</code>", MessageID)
            print("[ LGR ] : The news is fake")
    
    def RFC(self, CommandToReplace, RecievedMsg, context, update, MessageID):

        q = list()
        query = ValidQuery(RecievedMsg, CommandToReplace, context)

        query = self.stemming(query)
        q.append(query)

        vectorizer = TfidfVectorizer()                                          # Tf : term frequency (ie. counts the number of times a word is repeating in a document and so it understands that a word is important and assigns it a value) and idf: inverse document frequency (Detects the words which are repeating and dont have significant value and assigns it a lesser important values (Avengers))
        vectorizer.fit(q)

        q = self.vectorizer.transform(q)
        X_news = q

        prediction = self.clf.predict(X_news)

        print(prediction)

        if prediction[0] == 0:
            SendMessage.SendMessage(update, context, f"News status : <code>REAL</code> \nEngine : <code>KNeighborsClassifier</code> \nTest model accuracy : <code>{self.test_data_accuracy_CLF}</code>", MessageID)
            print('The news is real')
        else:
            SendMessage.SendMessage(update, context, f"News status : <code>FAKE</code> \nEngine : <code>KNeighborsClassifier</code> \nTest model accuracy : <code>{self.test_data_accuracy_CLF}</code>", MessageID)
            print("The news is fake")

######################################################################################################################################################################################

def ValidQuery(RecievedMsg, CommandToReplace, context):
    CommandWithBotname = CommandToReplace + context.bot.bot.name
    query = RecievedMsg.replace(f'/{CommandWithBotname}', '').replace(f'/{CommandToReplace}', '')
    query = query.strip()

    if(query == ''):
        return None
    else:
        return query

def EditMessage(msg, TextToUpdate):
    msg.edit_text(TextToUpdate, parse_mode=ParseMode.HTML)

def CreateMessage():
    MsgToSend = f"""   """

    return MsgToSend
