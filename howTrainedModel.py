#based on https://github.com/Ashwin-Dhakal/real-time-tweet-sentiment-analysis/blob/master/pickling%20all%20the%20classifier.py
import csv
from nltk.tokenize import word_tokenize
import nltk
import random
import pickle
tw = []
i = 0
with open('yourTrainingData.csv', newline='', encoding="latin-1") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if i > 100000:
            break
        if int(row[0]) == 0:
            i = i + 1
            tw.append((row[5],'neg'))
        elif int(row[0]) == 4:
            i = i + 1
            tw.append((row[5],'pos'))
csvfile.close()

mostFrequentWords = []
with open('mostFrequentWords.txt', 'r', encoding="latin-1") as f:
    for line in f:
        mostFrequentWords.append(line.strip())

def find_features(tweet):
    wordsFromTweet = word_tokenize(tweet)
    features = {}
    for word in mostFrequentWords:
        features[word] = (word in wordsFromTweet)
    return features

featuresets = [(find_features(tweetText), category) for (tweetText, category) in tw]
random.shuffle(featuresets)
testing_set = featuresets[90000:]
training_set = featuresets[:90000]

classifier = nltk.NaiveBayesClassifier.train(training_set)

save_classifier = open("trainedClassifier.pickle","wb")
pickle.dump(classifier,save_classifier)
save_classifier.close()