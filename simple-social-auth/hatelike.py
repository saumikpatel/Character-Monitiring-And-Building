from nltk.tokenize import sent_tokenize,word_tokenize
from collections import defaultdict
import operator
from empath import Empath
import re

def hateLikeMaker(tweets):
    lexicon = Empath()
    likeness = defaultdict(int)
    
    for i in tweets:
        sents = sent_tokenize(i)
        for j in sents:
            j = re.sub(r'[^\w\s]','',j)
            a = lexicon.analyze(j)
            if a['negative_emotion'] == 1:
                print("TRUE")
                for k, l in a.items():
                    if l == 1 and j != 'negative_emotion':
                        likeness[k] -= 1
            else:
                print("FALSE")
                for k, l in a.items():
                    if l == 1:
                        likeness[k] += 1
        if 'hate' in likeness:
            likeness.pop('hate')
        if 'envy' in likeness:
            likeness.pop('envy')
        likeness = sorted(likeness.items(), key=operator.itemgetter(1))
        dislikes = likeness[:3]
        length = len(likeness)
        likes = likeness[length - 3:length]
        likes = dict(likes)
        dislikes = dict(dislikes)
        return likes, dislikes