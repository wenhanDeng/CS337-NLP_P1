from processTweets import Newname2name, process_tweet
from textblob import TextBlob
from data import handle_Data

import spacy
import re
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
exclude_words = ['best', 'supporting']

def getSentiment(year):
    year = int(year)
    awards2tweets, useless, Newname2name = process_tweet(year)
    result = dict()
    if year == 2013 or year == 2015:
        awards_list = OFFICIAL_AWARDS_1315
    elif year == 2018 or year == 2019:
        awards_list = OFFICIAL_AWARDS_1819
    for award in awards_list:
        result[award] = "neutral"
    #Sentiment analysis for each award
   
    for key in awards2tweets:
        #total polarity score for each award
        socre = 0
        orname = Newname2name[key]
        #temp = name2Newname[award]
        temo = " "
        # temp = "".join(temp)
       
        tweets = awards2tweets[key]
        for tweet in tweets:
            tplist = tweet.split()
            for word in exclude_words:
                tplist = [w for w in tplist if w.lower() != word]
            sentence = " ".join(tplist)
            analysis = TextBlob(sentence)
            #socre += analysis.sentiment.polarity
            if analysis.sentiment.polarity > 0:
                socre += 1
            if analysis.sentiment.polarity < 0:
                socre -= 1
        if socre > 0:
            result[orname] = "positive"
        elif socre < 0:
            result[orname] = "negative"
        else:
            result[orname] = "neutral"
   # print(result)
    return result
        


#getSentiment(2015)
