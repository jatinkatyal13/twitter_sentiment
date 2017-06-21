
# coding: utf-8

# In[6]:

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import oauth2client
import oauth2
import twitter
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


# In[7]:

api = twitter.Api(consumer_key='c5PWC3zeqDtcUiX5WilOranXL',
                      consumer_secret='SaIx1DH4nfekCVmdz69sh7y4yv5UOk6WNHzBYinTidIBeSkPcc',
                      access_token_key='4332692365-5WxA1pYMkaKVqYiCDauOtKf8YtKlwmbqasZbyO3',
                      access_token_secret='au8ErKdjWSfW191kwye5Lagm4mwtD16PNX9Fnrgb7t0IJ')


# In[8]:

def get_tweet_sentiment(tweet):
       
        analysis = TextBlob(clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


# In[9]:

def clean_tweet(tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# In[10]:

hand = ['CSIR_4PI','CBRIRoorkee','CSIRofficial','CSIR_CECRI','CSIRICC','socialniscair','IGIB_DEL_110007',
       'CSIR_CCMB','CSIR_CDRI','CSIRCEERI','csircftri','official_cgcri',
        'CSIRCIMAP','CSIR_CIMFR','CSIR_CMERI','CSIRCRRI','CSIR_CSIO','csircsmcri','CSIR_IHBT','IICBKolkata',
        'csiriict','csiriiim','CSIRIIP','csiryimmt','CSIR_IMTECH','CSIR_IITR','csirnbrilko','csir_ncl',
        'DirectorNEERI','CSIRNIGOA','csirngri','csirnistads','CSIR_NPL','CSIR_NML','CSIR_NEIST','osdd',
        'csir_niist','csir_serc','patinformatics','csirampribhopal','CSIR_IND']


# In[11]:

def tor(final):
    new = []

    total = len(final)
    total = float(total)

    pos = 0.0
    neg = 0.0
    neu = 0.0

    for tweet in final:
        bclear = tweet.text
        aclear = clean_tweet(bclear)
        ablob = TextBlob(aclear)
        sent = ablob.sentiment.polarity
        if(sent > 0):
            pos = pos+1
        elif(sent == 0):
            neu = neu+1
        else:
            neg = neg+1
    
    if total > 0:
        posper = pos/total*100
        negper = neg/total*100
        neuper = neu/total*100
        polar = [posper,negper,neuper]
    else:
        polar = [0, 0, 0]
    
    return(polar)


# In[12]:



def getRes(choice, query):

    a = []
    b = []

    if choice==1:
        
        s = "q="+query
        final = api.GetSearch(raw_query=s)
        a = tor(final)
        
    elif choice==2:
        
        s = "q=%23"+query
        final = api.GetSearch(raw_query=s)
        a = tor(final)
        
    elif choice==3:
        
        s = "q=%40"+query
        final = api.GetSearch(raw_query=s)
        a = tor(final)
        
    else:
        for handle in hand:
            s = "q=%40"+handle
            final = api.GetSearch(raw_query=s)
            if not final:
                a.append([0,0,0])
                continue
            b = tor(final)
            a.append(b)

    return a
        


def getSentimentGraph (option, query):

    # option:
    #     0 Hashtag
    #     1 String
    #     2 Handle
    #     3 All CSIR


    # calculate

    option = int(option)

    r = getRes(option, query)
    res = [
        ['Handle'.encode('utf-8'), 'Positive'.encode('utf-8'), 'Negative'.encode('utf-8'), 'Neutral'.encode('utf-8')]
    ]
    if option != 4:
        res = [
            ["Sentiment".encode('utf-8'), "Number".encode('utf-8')],
            ["Positive".encode('utf-8'), r[0]],
            ["Negative".encode('utf-8'), r[1]],
            ["Neutral".encode('utf-8'), r[2]],
        ]

    else:
        for i in range(len(r)):
            res.append([
                hand[i].encode('utf-8'),
                r[i][0],
                r[i][1],
                r[i][2]
            ])


    return res


