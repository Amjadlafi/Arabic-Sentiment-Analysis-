# -*- coding: utf-8 -*-
"""
This script builds BoW representations for all the tweets 
based on vocab.txt
"""
import re
import json
from string import punctuation
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
 

# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r' , encoding='utf8')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text


def removeNonArabicLetters(ArabicText):
    return re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', ArabicText)

# turn a tweet into clean tokens
def clean_tweet(tw):
    #remove non-Arabic text    
    tw = removeNonArabicLetters(tw)
	# split into tokens by white space
    tokens = tw.split()
	# remove punctuation from each token
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
	# filter out stop words
    stop_words = set(stopwords.words('arabic'))
    tokens = [w for w in tokens if not w in stop_words]
	# filter out short tokens
    tokens = [word for word in tokens if len(word) > 2]
    return tokens


# clean tweet, remove any word not in vocab and return line of tokens
def filter_by_vocab(tweet , vocab):
	# clean doc
	tokens = clean_tweet(tweet)
	# filter by vocab
	tokens = [w for w in tokens if w in vocab]
	return ' '.join(tokens)
    
    
# load tweet dictionary and clean tweets
def process_tweets(tweet_filename, vocab):
    lines = list()
    with open(tweet_filename , 'r' , encoding='utf8') as json_file:
        tweets = json.load(json_file)
    
	# walk through all tweets
    for tw in tweets.values():
        # filter the tweet
        line = filter_by_vocab(tw, vocab)
        # add to list
        lines.append(line)
        
    return lines



if __name__ == "__main__":
    
    #1. load the vocabulary
    vocab_filename = 'vocab.txt'
    vocab = load_doc(vocab_filename)
    vocab = vocab.split()
    vocab = set(vocab)

    #2. process tweets based on the vocab
    pos_tweets_lines = process_tweets('pos_tweets.json', vocab)
    neg_tweets_lines = process_tweets('neg_tweets.json', vocab)
    neu_tweets_lines = process_tweets('neu_tweets.json', vocab)
    
    #3. produce Bag-of-words represenation
    # create the tokenizer
    tokenizer = Tokenizer()
    # fit the tokenizer on all tweets
    all_tweets  = pos_tweets_lines + neg_tweets_lines + neu_tweets_lines
    tokenizer.fit_on_texts(all_tweets)
    
    # encode tweets 
    bow = tokenizer.texts_to_matrix(all_tweets, mode='freq')
    print(f'The size of BoW representation = {bow.shape}')
 