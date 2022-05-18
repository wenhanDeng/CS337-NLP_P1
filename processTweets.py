
from data import handle_Data
from gg_api import OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819
import spacy
import re

words_exclusion = ['-', 'performance', 'of', 'by', 'an', 'in', 'a', 'an', 'role', 'best', 'made', 'for']

awards2tweets = {}
awards2newAward = {}
name2newName = {}
def process_tweet(years):
    nlp = spacy.load('en_core_web_sm')
    if years == 2013 or years == 2015:
        awards_list = OFFICIAL_AWARDS_1315
    elif years == 2018 or years == 2019:
        awards_list = OFFICIAL_AWARDS_1819
    # process the award name first
    new_awards_list = []
    for a in awards_list:
        new_name = []
        for i in a.split():
            if i in words_exclusion:
                continue
            else:
                new_name.append(i)
        new_awards_list.append(new_name)
        name2newName[a] = new_name

    # modify the award key name
    for a in new_awards_list:
        if "television" in a:
            a.append('tv')
        if "cecil" in a:
            a.append('lifetime')
            a.append('pre-lifetime')
            a.append('achievement')
        
  
    result = handle_Data(years)
    for t in result:
        tweet = t.lower()
        for a in new_awards_list:
            award_name = ''.join(a)
            # print(award_name)
            count = 0
            if 'actor' in a and tweet.find('actor') == -1:
                continue

            elif 'actress' in a and tweet.find('actress') == -1:
                continue
            
            elif 'director' in a and tweet.find('director') == -1:
                continue
            
            elif 'drama' in award_name and (('comedy' or 'musical') in tweet):
                continue
            
            elif (('comedy' or 'musical') in award_name) and 'drama' in tweet:
                continue   

            elif 'supporting' in a and tweet.find('supporting') == -1:
                continue      

            elif 'supporting' not in a and tweet.find('supporting') != -1:
                continue 

            elif 'tv' in a and (tweet.find('tv') == -1 and tweet.find('television') == -1):
                continue  
            
            elif 'tv' not in a and (tweet.find('tv') != -1 or tweet.find('television') != -1):
                continue  
            
            elif 'mini-series' in a and (tweet.find('mini') == -1):
                continue  
            
            elif 'mini-series' not in a and (tweet.find('mini') != -1):
                continue 
            
            elif 'score' not in a and (tweet.find('score') != -1):
                continue 
            
            elif 'song' not in a and (tweet.find('song') != -1):
                continue 
            
            elif 'score' in a and (tweet.find('score') == -1):
                continue 
            
            elif 'song'  in a and (tweet.find('song') == -1):
                continue 
            
            elif 'screenplay'  in a and (tweet.find('screenplay') == -1):
                continue 
            
            elif 'screenplay' not in a and (tweet.find('screenplay') != -1):
                continue

            # elif (tweet.find('actor') != -1 or tweet.find('actress') != -1) and 'actress' not in a:
            #     continue  
            else:
                for w in a:
                    if tweet.find(w) != -1:
                        count += 1
                if len(a) <= 3 and count >= len(a):
                    if award_name in awards2tweets:
                        awards2tweets[award_name].append(t)
                    else:
                        awards2tweets[award_name] = []
                        awards2tweets[award_name].append(t)
                elif len(a) > 3 and count >= len(a) - 2:
                    if award_name in awards2tweets:
                        awards2tweets[award_name].append(t)
                    else:
                        awards2tweets[award_name] = []
                        awards2tweets[award_name].append(t)

    # print(new_awards_list)            
    return awards2tweets, new_awards_list, name2newName


process_tweet(2013)