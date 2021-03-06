
from processTweets import Newname2name, process_tweet
from winner import getWinners
from hosts import findhosts
import spacy
import re
from data import handle_Data


def find_presenter(year):
    year = int(year)
    # load english language model
    awards2tweets, awards_list, Newname2name = process_tweet(year)
    PRESENT_WORDS = ['present', 'presents', 'presenters', 'presenting', 'introduces', 'intros', 'introducing', 'announce', 'announcing', 'announcers','mentions', 'mentioned', 'mention', 'award', 'awarded', 'awarding']
    tem = ['best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance']
    name_pattern = re.compile(r'[A-Z][a-z]* [A-Z][a-z]*')
    hosts = findhosts(year)
    
   
    result = {}
    other_people = hosts
    for award in awards2tweets:
        presenters = {}
        tweets = awards2tweets[award]
        nlp = spacy.load('en_core_web_sm')
        presenter = {}
        for text in tweets:
            words = text.split()
            found = False
            for word in words:
                if word.lower() in PRESENT_WORDS:
                    found = True;
                    break;
            if found:
                output = name_pattern.findall(text)
                for names in output:
                    if 'Golden Globe' in names:
                        continue
                    na = names.lower()
                    if any([t in na for t in tem]):
                        continue
                    if na in other_people:
                        continue

                    if na in presenters:
                        presenters[na] += 1
                    else:
                        presenters[na] = 1
                # for names in output.ents: 
                #     if names.label_ == 'PERSON':
                #         name = names.text.lower()
                #         if name not in other_people:
                #             if name in presenters:
                #                 presenters[name] += 1
                #             else:
                #                 presenters[name] = 1
        
        presenters = sorted(presenters.items(), key = lambda kv:kv[1], reverse= True)
        presenters = presenters[:2]
        presenters = list(map(list, presenters))
        
        
        presenters_name = []
        for presenter in presenters:
            presenters_name.append(presenter[0])
        if len(presenters_name) > 1:
            if presenters[0][1] * 1.0 / presenters[1][1] > 2:
                presenters_name = presenters_name[:1]
            else:
                presenters_name = presenters_name[:2]
        result[award] = presenters_name
    result2 = {}
    for award in result:
        result2[Newname2name[award]] = result[award]
    return result2
    
    
  
#find_presenter(2013)

