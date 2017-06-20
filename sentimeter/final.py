
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
a = []
b = []


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



print("1.String 2.Hashtag 3.Handle 4.ALL CSIR handles")
choice = input()

if(choice==1):
    
    print("Enter string")
    s = "q="+raw_input()
    final = api.GetSearch(raw_query=s)
    a = tor(final)
    
elif(choice==2):
    
    print("Enter Hashtag")
    s = "q=%23"+raw_input()
    final = api.GetSearch(raw_query=s)
    a = tor(final)
    
elif(choice==3):
    
    s = "q=%40"+raw_input()
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
            
    print "done !"     
        


# In[14]:

poslist = []
neglist = []
neulist = []

for i in range(len(a)):
    poslist.append(a[i][0])
    neglist.append(a[i][1])
    neulist.append(a[i][2])
    


# In[19]:

import numpy as np
import matplotlib.pyplot as plt

N = 41
ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars
opacity = 0.4

fig = plt.figure(figsize=(30,12))
ax = fig.add_subplot(111)

#yvals = [32,34,36,28,40,42,44]
yvals = poslist
rects1 = ax.bar(ind, yvals, width, color='g')
#zvals = [2,4,6,8,10,12,14]
zvals = neglist
rects2 = ax.bar(ind+width, zvals, width,color='r')
#kvals = [1,2,3,4,5,6,7]
kvals = neulist
rects3 = ax.bar(ind+width*2, kvals, width, color='b')

ax.set_ylabel('Polarity')
ax.set_xticks(ind+width)
ax.set_xticklabels( hand )
ax.legend( (rects1[0], rects2[0], rects3[0]), ('pos', 'neg', 'neu') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')


plt.show()


# In[32]:

import numpy as np
import matplotlib.pyplot as plt

N = 41
ind = np.arange(N)  # the x locations for the groups
width = 0.3       # the width of the bars
opacity = 0.4

fig = plt.figure(figsize=(30,30))
ax = fig.add_subplot(111)

#yvals = [32,34,36,28,40,42,44]
yvals = poslist
rects1 = ax.barh(ind, yvals, width, color='g')
#zvals = [2,4,6,8,10,12,14]
zvals = neglist
rects2 = ax.barh(ind+width, zvals, width,color='r')
#kvals = [1,2,3,4,5,6,7]
kvals = neulist
rects3 = ax.barh(ind+width*2, kvals, width, color='b')

ax.set_xlabel('Polarity')
ax.set_yticks(ind+width)
ax.set_yticklabels( hand )
ax.legend( (rects1[0], rects2[0], rects3[0]), ('pos', 'neg', 'neu') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom')


plt.show()


def getSentimentGraph (option, query):

    # option:
    #     0 Hashtag
    #     1 String
    #     2 Handle
    #     3 All CSIR


    # calculate


    return [
        ['Sentiment', 'No. of Tweets'],
        ['Positive', positive_count],
        ['Neutral', neutral_count],
        ['Negative', negative_count],
    ]


