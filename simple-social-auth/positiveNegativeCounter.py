from textblob import TextBlob
from nltk.tokenize import sent_tokenize,word_tokenize
import time


def posNegCounter(tweets):
    rtweets = []
    ptweets = {}
    for i in tweets:
        # text = "I love music. I love to dance. I hate to code though. I hate everything else."
        sent_text = sent_tokenize(i)
        for i in sent_text:
            a = TextBlob(i)
            ptweets['text'] = a.string
            if a.sentiment.polarity > 0:
                ptweets['sentiment'] = "Positive"   
            elif a.sentiment.polarity == 0:
                ptweets['sentiment'] = "Neutral"
            else:
                ptweets['sentiment'] = "Negative"
            rtweets.append(dict(ptweets))
    positive = [i['text'] for i in rtweets if i['sentiment'] == 'Positive']
    negative = [i['text'] for i in rtweets if i['sentiment'] == 'Negative']
    
    posPercent = 100*len(positive)/len(rtweets)
    negPercent = 100*len(negative)/len(rtweets)

    positive = positive[:3]
    negative = negative[:3]
    
    return posPercent, negPercent, positive, negative