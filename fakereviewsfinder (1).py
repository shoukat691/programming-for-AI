# -*- coding: utf-8 -*-
"""FakeReviewsFinder

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lzEt2Rbx7mrooI6cIFB7j7bSMknLdGmA
"""

import numpy as np
import pandas as pd
import re
import nltk


path = "/content/drive/MyDrive/DataSets/Restaurant_Reviews.csv"


try:
    dataset = pd.read_csv(path, delimiter=',', quoting=3, engine='python', error_bad_lines=False)
    print("Dataset loaded successfully.")
except Exception as e:
    print("Error reading the CSV file:", e)
    dataset = None

if dataset is not None:

    print(dataset.head(2))


    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer


    ps = PorterStemmer()


    corpus = []
    for i in range(0, 1000):

        review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
        review = review.lower()
        review = review.split()


        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)


    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=1500)
    X = cv.fit_transform(corpus).toarray()


    y = dataset.iloc[:1000, 1].values


    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)


    from sklearn.svm import SVC
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(X_train, y_train)


    y_pred = classifier.predict(X_test)


    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)


    accuracy = round((cm[0, 0] + cm[1, 1]) / np.sum(cm), 2)
    precision = round(cm[1, 1] / (cm[1, 1] + cm[0, 1]), 2)
    recall = round(cm[1, 1] / (cm[1, 1] + cm[1, 0]), 2)
    f1_score = round((2 * precision * recall) / (precision + recall), 2)


    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1_score}")

