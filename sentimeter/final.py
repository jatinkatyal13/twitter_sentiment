
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

api = twitter.Api(consumer_key='iXZyChJoFTYpsJl765BUn3F4o',
                      consumer_secret='BZZ5gasUplbBTsmNjwQVv52xrnl41aMg94gRkqAAJ5fcu95daa',
                      access_token_key='2794625946-BGeQbC4Xu2v3Vwa9hTrwiOsiEHMFX2LjxgVgQU1',
                      access_token_secret='ZThu9UaQsRSAsjaz5QdhVQyqbPjSUM9c8ArO7rnyA7MmS')


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
    
    posper = pos/total*100
    negper = neg/total*100
    neuper = neu/total*100
    
    polar = [posper,negper,neuper]
    
    return(polar)


# In[12]:



def getRes(choice, query):

    a = []
    b = []

    if(choice==1):
        
        s = "q="+query
        final = api.GetSearch(raw_query=s)
        a = tor(final)
        
    elif(choice==2):
        
        s = "q=%23"+query
        final = api.GetSearch(raw_query=s)
        a = tor(final)
        
    elif(choice==3):
        
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
    r = getRes(option, query)
    res = {}
    if option != 4:
        res[query] = {
            'pos' : r[0],
            'neg' : r[1],
            'neu' : r[2]
        }

    else:
        for i in range(len(r)):
            res[hand[i]] = {
                'pos' : r[i][0],
                'neg' : r[i][1],
                'neu' : r[i][2]
            }


    return res


