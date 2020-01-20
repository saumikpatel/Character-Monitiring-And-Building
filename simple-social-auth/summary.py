from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk
from words import someWords
import re


min_cut = 0.1
max_cut = 1.0
stopwords = set(stopwords.words('english') + list(punctuation))
n = 5
mainTweets = []
def summaryMaker(tweets, badWords):
    for i in tweets:
        # PUNCTUATION REMOVER
        s = re.sub(r'[^\w\s]','',i)
        mainTweets.append(s)
        text = ". ".join(mainTweets)
    n = 5
    # SENTENCE TOKENIZE
    sents = sent_tokenize(text)
    assert n <= len(sents)
    # WORD TOKENIZE
    word_sent = [word_tokenize(s.lower()) for s in sents]
    # FREQUENCY
    freq = defaultdict(int)
    for i in word_sent:
        for j in i:
    #         print(j)
            if j in someWords:
                badWords += 1
            if j not in stopwords:
                freq[j] += 1
    # Get max used words
    maximum = nlargest(5, freq, key=freq.get)
    #     Normalization        
    m = float(max(freq.values()))
    for w in list(freq):
        freq[w] = freq[w]/m
        if freq[w] >= max_cut or freq[w] <= min_cut:
            del freq[w]

    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
        for w in sent:
            if w in freq:
                ranking[i] += freq[w]
    sents_idx = nlargest(n, ranking, key=ranking.get)

    summary = [sents[j] for j in sents_idx]
    summary = ". ".join(summary)
    percent = (badWords / len(someWords)) * 100
    return summary, badWords, percent, maximum