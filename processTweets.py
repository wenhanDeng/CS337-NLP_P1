
from data import handle_Data
import spacy
import re
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
words_exclusion = ['-', 'performance', 'of', 'by', 'an', 'in', 'a', 'an', 'role', 'best', 'made', 'for']

awards2tweets = {}
awards2newAward = {}
Newname2name = {}
def process_tweet(years):
    nlp = spacy.load('en_core_web_sm')
    cur_awards_list = []
    if years == 2013 or years == 2015:
        cur_awards_list = OFFICIAL_AWARDS_1315
    elif years == 2018 or years == 2019:
        cur_awards_list = OFFICIAL_AWARDS_1819
    # process the award name first
    new_awards_list = []
    for a in cur_awards_list:
        new_name = []
        for i in a.split():
            if i in words_exclusion:
                continue
            else:
                new_name.append(i)
        if "television" in a:
            new_name.append('tv')
        if "cecil" in a:
            new_name.append('lifetime')
            new_name.append('pre-lifetime')
            new_name.append('achievement')
        new_awards_list.append(new_name)
        Newname2name[''.join(new_name)] = a

    # modify the award key name

        
  
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
    return awards2tweets, new_awards_list, Newname2name

