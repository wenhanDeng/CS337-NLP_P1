from data import handle_Data
import re
from textblob import TextBlob

def findbestandwrostdressed(year):
    tweets = handle_Data(year)
    name_pattern = re.compile(r'[A-Z][a-z]* [A-Z][a-z]*')
    bestdressed = dict()
    worstdressed = dict()
    for tweet in tweets:
        if "best dressed" in tweet.lower():
            analysis = TextBlob(tweet)
            if analysis.sentiment.polarity > 0:
                navie = name_pattern.findall(tweet)
                for names in navie:
                    if 'Golden Globe' in names:
                        continue
                    if 'Best Dressed' in names or 'Worst Dressed' in names:
                        continue
                    na = names.lower()
                    if na in bestdressed:
                        bestdressed[na] += 1
                    else:
                        bestdressed[na] = 1
            else:
                continue
        elif "worst dressed" in tweet.lower():
            analysis = TextBlob(tweet)
            if analysis.sentiment.polarity <= 0:
                navie = name_pattern.findall(tweet)
                for names in navie:
                    if 'Golden Globe' in names:
                        continue
                    if 'Worst Dressed' in names or 'Best Dressed' in names:
                        continue
                    na = names.lower()
                    if na in worstdressed:
                        worstdressed[na] += 1
                    else:
                        worstdressed[na] = 1
            else:
                continue
    #print(max(bestdressed, key=bestdressed.get))
    #print(max(worstdressed, key=worstdressed.get))
    result = [max(bestdressed, key=bestdressed.get),max(worstdressed, key=worstdressed.get)]
    #print(result)
    return result       

#findbestandwrostdressed(2013)