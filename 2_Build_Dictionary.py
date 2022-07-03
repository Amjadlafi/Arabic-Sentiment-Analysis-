# -*- coding: utf-8 -*-

"""
This script generate the vocab for the tweets
"""
import re
from string import punctuation
from nltk.corpus import stopwords
from collections import Counter
import json


"""
Detect all Arabic Characters:

/[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]/

Summary:

  Arabic (0600—06FF, 225 characters)

  Arabic Supplement (0750—077F, 48 characters)

  Arabic Extended-A (08A0—08FF, 39 characters)

  Arabic Presentation Forms-A (FB50—FDFF, 608 characters)

  Arabic Presentation Forms-B (FE70—FEFF, 140 characters)

  Rumi Numeral Symbols (10E60—10E7F, 31 characters)

  Arabic Mathematical Alphabetic Symbols (1EE00—1EEFF, 143 characters)


Example:
    regex instruction to keep arabic and numeric chars and remove the rest:


import re
text = "llll 2.36 aaan ششم  . ,^  . %1563"

t = re.sub(r'[^0-9\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', text)

"""
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

#process a dictionary of tweets
#extracts the vocab and stores them in vocab
def process_tweets(tweet_dictionary, vocab):
    
    for tweet_text in tweet_dictionary.values():
        # clean doc
        tokens = clean_tweet(tweet_text) 
        # update counts
        vocab.update(tokens)
        
    
# save list to file
def save_list(lines, filename):
	# convert lines to a single blob of text
	data = '\n'.join(lines)
	# open file
	file = open(filename, 'w' , encoding='utf8')
	# write text
	file.write(data)
	# close file
	file.close()
 



if __name__ == "__main__":
    # define vocab data structure as Counter
    vocab = Counter()

    #load json files
    with open('pos_tweets.json', 'r', encoding='utf8') as json_file:
        pos_tweets = json.load(json_file)

    with open('neg_tweets.json', 'r', encoding='utf8') as json_file:
        neg_tweets = json.load(json_file)

    with open('neu_tweets.json', 'r', encoding='utf8') as json_file:
        neu_tweets = json.load(json_file)
    
    
    process_tweets(pos_tweets, vocab)
    process_tweets(neg_tweets, vocab)
    process_tweets(neu_tweets, vocab)

    # print the size of the vocab
    print(len(vocab))
    # print the top words in the vocab
    print(vocab.most_common(50))

    # keep tokens with a min occurrence
    min_occurane = 2
    tokens = [k for k,c in vocab.items() if c >= min_occurane]
    print(len(tokens))

    # save tokens to a vocabulary file
    save_list(tokens, 'vocab.txt')