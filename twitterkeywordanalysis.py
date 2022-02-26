
# Twitter Keyword Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tweepy

# API Removed
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

keyword = "cryptocurrency"
# To print tweets:
# tweets = api.search_tweets(keyword)
# for tweet in tweets:
    # print(tweet.entities['user_mentions'])
    #print(tweet.entities['hashtags'])
    # print(tweet.text)

columns = ['created', 'tweet_text']
df = pd.DataFrame(columns=columns)

tweets = api.search_tweets(keyword)
for tweet in tweets:
    tweet_text = tweet.text
    created = tweet.created_at
    row = [created, tweet_text]
    series = pd.Series(row, index=df.columns)
    df = df.append(series, ignore_index=True)
        
print("Get data 100% complete..")
df.head()

# Text Cleaning using regular expressions
## English stopwords drawn from https://gist.github.com/sebleier/554280.
## Text cleaning is also possible through the NLTK (Natural Language Toolkit) library - this code just did it directly for better conceptual understanding.
## For instance, stopwords can be found by "from nltk.corpus import stopwords"
## Chunk below was included for future reference

import re
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import TweetTokenizer

def text_cleaning(text):
    temp = text.lower()
    temp = re.sub("'", "", temp)
    temp = re.sub("@[A-Za-z0-9_]+", "", temp)
    temp = re.sub("^rt", "", temp)
    temp = re.sub("#[A-Za-z0-9_]+", "", temp)
    temp = re.sub(r"http\S+", "", temp)
    temp = re.sub(r"www.\S+", "", temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]', ' ', temp)
    temp = re.sub("[^a-z0-9]", " ", temp)
    temp = temp.split()
    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp

df['eng_text'] = df['tweet_text'].apply(lambda x: text_cleaning(x))
df.head()

# Making the WordCloud
from wordcloud import WordCloud

# Frequency of words
fdist = FreqDist(df['eng_text'])

# WordCloud
wc = WordCloud(width=800, height=400, max_words=50).generate_from_frequencies(fdist)
plt.figure(figsize=(12,10))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()