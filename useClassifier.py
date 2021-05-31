import pandas as pd
import json
import string
from nltk.tokenize import TweetTokenizer as TT, word_tokenize
from nltk.tokenize.casual import remove_handles
import validators
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import pickle
from nltk.corpus import stopwords

def GetTokens(text):
    tokens = tweetTokenizer.tokenize(remove_handles(text))
    for i in range(len(tokens)-1,-1,-1):    
        if tokens[i] in string.punctuation or ord(tokens[i][0])>127 or validators.url(tokens[i]) or tokens[i] in stopWords:
            del tokens[i]
    return tokens

def LemmatizeTokens(tokens):
    wordLemmatizer = WordNetLemmatizer()
    for index, tuple in enumerate(pos_tag(tokens)):
        if tuple[1].startswith("V"):
            tokens[index] = wordLemmatizer.lemmatize(tuple[0],"v")
        elif tuple[1].startswith("J"):
            tokens[index] = wordLemmatizer.lemmatize(tuple[0],"a")
        elif tuple[1].startswith("R"):
            tokens[index] = wordLemmatizer.lemmatize(tuple[0],"r")
        elif tuple[1].startswith("P"):
            continue
        else:
            tokens[index] = wordLemmatizer.lemmatize(tuple[0],"n")
    return tokens

def GetFeatures(tweet):
    wordsFromTweet = tweetTokenizer.tokenize(tweet["Tweet_text"])
    features = {}
    for word in mostFrequentWords:
        features[word] = (word in wordsFromTweet)
    return features

def GetClassifier():
    classifier_f = open("path\\to\\classifier","rb")
    c = pickle.load(classifier_f)
    classifier_f.close()
    return c

def CreateDataFrame(tweets):

    classifier = GetClassifier()
    for tweet in tweets:
        rawTokens = GetTokens(tweet["Tweet_text"])
        
        lemmatizedTokens = LemmatizeTokens(rawTokens)
        for i in range(len(lemmatizedTokens)-1, -1, -1):
            if len(lemmatizedTokens[i]) < 2 or lemmatizedTokens[i].isnumeric()  or lemmatizedTokens[i].lower() in swearWords:
                del lemmatizedTokens[i]
                continue
            lemmatizedTokens[i] = lemmatizedTokens[i].replace("\'", "")
        pandaFrameData["text"].append(" ".join(lemmatizedTokens))
        pandaFrameData["id"].append(tweet["Tweet_id"])
        pandaFrameData["date"].append(tweet["Tweet_creation"])
        
        # Appends pos/neg to dataFrame
        # Finds features from a tweets, returns a tuple ( [], '' )    
        # Passes it to classifier which needs a feature set.
    
        featureSet = (GetFeatures(tweet), 'unknown')[0] 
        pandaFrameData["sentiment"].append(classifier.classify(featureSet)) 

def GetTweets():
    file = open("path\\to\\tweets","r+")
    return json.load(file)['tweets']

def GetMostFrequentWords(mostFrequentWords):
    with open('path\\to\\mostFrequentWords', 'r', encoding="latin-1") as f:
        for line in f:
            mostFrequentWords.append(line.strip())
    f.close()
    return mostFrequentWords

def GetSwearWords():
    with open('path\\to\\swear\\words', 'r', encoding="latin-1") as f:
        for line in f:
            swearWords.append(line.strip())
    f.close()
    return swearWords
# ---------------------------------------------- MAIN PROGRAM ------------------------------------------

pandaFrameData = {"text":[],"id":[], "sentiment":[], "date":[]}
mostFrequentWords = []
swearWords = []
tweetTokenizer = TT()
if __name__ == "__main__":
    stopWords = set(stopwords.words("english"))
    tweetsFromFile = GetTweets()
    swearWords = GetSwearWords()
    mostFrequentWords = GetMostFrequentWords(mostFrequentWords)

    CreateDataFrame(tweetsFromFile)
    sportTweets = pd.DataFrame(pandaFrameData,columns = list(pandaFrameData.keys()))
    print(sportTweets)
    
