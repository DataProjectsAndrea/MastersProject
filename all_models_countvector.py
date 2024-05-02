# -*- coding: utf-8 -*-
"""All_models_countvector.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tmPGIqesUdigJXjw1O-HXC4cUMFhq_2y
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

np.random.seed(500)
Corpus = pd.read_csv(r"/content/balanced_100_words_train.csv",encoding='latin-1')
sep_test = pd.read_csv(r"/content/balanced_100_words_test.csv", encoding='latin-1')

# Confirm no blank rows
Corpus['texts'].dropna(inplace=True)

Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['texts'],Corpus['label'],test_size=0.3, random_state=16)

# create the vocabulary
vectorizer = CountVectorizer()
vectorizer.fit(Corpus['texts'])
Train_countV = vectorizer.transform(Train_X)
Test_countV = vectorizer.transform(Test_X)

# prep test set

Val_countV = vectorizer.transform(sep_test['texts'])
val_y = sep_test['label']

# fit the training dataset on the NB classifier
Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_countV,Train_Y)

# predict the labels on validation dataset
predictions_NB = Naive.predict(Test_countV)

#val set
predictions_NB_val = Naive.predict(Val_countV)

# Use accuracy_score function to get the accuracy
print("Naive Bayes Accuracy Score -> ",accuracy_score(Test_Y, predictions_NB))
print("Naive Bayes F1 Score -> ",f1_score(Test_Y, predictions_NB))
print("Naive Bayes Accuracy Val Score -> ",accuracy_score(val_y, predictions_NB_val))

# print("Naive Bayes precision Val Score -> ",precision_score(val_y, predictions_NB_val))
# print("Naive Bayes recall Val Score -> ",recall_score(val_y, predictions_NB_val))
print("Naive Bayes F1 Val Score -> ",f1_score(val_y, predictions_NB_val))

# Classifier - Algorithm - SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(Train_countV,Train_Y)

# predict the labels on validation dataset
predictions_SVM = SVM.predict(Test_countV)
val_pred = SVM.predict(Val_countV)

# Use accuracy_score function to get the accuracy
print("SVM Accuracy Score -> ",accuracy_score(Test_Y, predictions_SVM))
print("SVM Accuracy Score Val Set -> ",accuracy_score(val_y, val_pred))
print("SVM F1 Score -> ",f1_score(Test_Y, predictions_SVM))
print("SVM F1 Score Val Set -> ",f1_score(val_y, val_pred))

SVM.fit(Train_countV, Train_Y)

predictions = SVM.predict(Test_countV)
cm = confusion_matrix(Test_Y, predictions, labels=SVM.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=SVM.classes_)
disp.plot()

plt.show()


#import pandas
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer

y_train = Train_Y
y_test = Test_Y

# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression(random_state=16)

# fit the model with data
logreg.fit(Train_countV, y_train)

y_pred = logreg.predict(Test_countV)

val_pred = logreg.predict(Val_countV)

score = accuracy_score(y_test,y_pred)
print('Log accuracy:',score)

score_val = accuracy_score(val_y, val_pred)
print('Log accuracy Val:',score_val)

score = f1_score(y_test,y_pred)
print('Log F1:',score)

score_val = f1_score(val_y, val_pred)
print('Log F1 Val:',score_val)

# import the metrics class
from sklearn import metrics

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
cnf_matrix

# import required modules
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix Log Regression', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
print(classification_report(y_test, y_pred))

y_pred_proba = logreg.predict_proba(Test_countV)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()

# Load libraries
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(Train_countV,y_train)

#Predict the response for test dataset
y_pred = clf.predict(Test_countV)

# val prediction
val_pred = clf.predict(Val_countV)

# Model Accuracy, how often is the classifier correct?
print("Decision Tree Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Decision Tree Val Accuracy:",metrics.accuracy_score(val_y, val_pred))
print("Decision Tree F1:",metrics.f1_score(y_test, y_pred))
print("Decision Tree Val F1:",metrics.f1_score(val_y, val_pred))

from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('text.png')
Image(graph.create_png())

#Importing MLPClassifier
from sklearn.neural_network import MLPClassifier

#Init the MLPClassifier
classifier = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=300,activation = 'relu',solver='adam',random_state=1)

#Fitting the training data to the network
classifier.fit(Train_countV,y_train)

#Using the trained network to predict

#Predicting y for X_val
y_pred = classifier.predict(Test_countV)

#Predicting y for X_val
val_pred = classifier.predict(Val_countV)

from sklearn.metrics import confusion_matrix
#Comparing the predictions against the actual observations in y_val
# double check set up cm = confusion_matrix(y_pred, y_test)

#Printing the accuracy
print("Accuracy of MLPClassifier : ", metrics.accuracy_score(y_test, y_pred))
print("Accuracy of Validation MLPClassifier : ", metrics.accuracy_score(val_y, val_pred))
print("F1 of MLPClassifier : ", metrics.f1_score(y_test, y_pred))
print("F1 of Validation MLPClassifier : ", metrics.f1_score(val_y, val_pred))


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(Train_countV,y_train)
y_pred = rf.predict(Test_countV)
val_pred = rf.predict(Val_countV)
accuracy = accuracy_score(y_test, y_pred)
val_accuracy = accuracy_score(val_y, val_pred)
F1 = f1_score(y_test, y_pred)
val_F1 = f1_score(val_y, val_pred)
print("Accuracy RF:", accuracy)
print("Val Accuracy RF:", val_accuracy)
print("F1 RF:", F1)
print("Val F1 RF:", val_F1)