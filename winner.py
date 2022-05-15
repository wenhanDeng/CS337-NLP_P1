
from lib2to3.pgen2 import token
from turtle import Turtle
from processTweets import process_tweet
from data import handle_Data
import spacy
import re
# nlp = spacy.load('en_core_web_sm')
# check = nlp('Daniel Day')
# sig = False
# for tok in check.ents:
#     if tok.label_ == 'PERSON':
#         print(tok.text)
 
def getWinners(year):
     
    awards2tweets, awards_list, name2Newname = process_tweet(year)
    for tt in awards2tweets:
     result = awards2tweets['actorsupportingseries,mini-seriesormotionpicturetelevisiontv']
     winner_keyword = ['win', 'won', 'goes to', 'go to', 'congrates', 'congratulations', 'congratulate', '-', 'for']
     tem = ['best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance', 'series', 'tv', 'mini', 'and', 'golden globe', 'song']
     nlp = spacy.load('en_core_web_sm')
     if ('actor' not in tt) and ('actress' not in tt) and ('cecil' not in tt) and ('director' not in tt):
         for out in result:
             o = nlp(out)
            #  for tok in o.ents:
            #     #  print(tok.text, '->', tok.label_)
     else:

      name_pattern = re.compile(r'[A-Z][a-z]* [A-Z][a-z]*')
      
      year_pattern = re.compile(r'\d{4}')
         
      hosts = {}
      total = 0
      for out in result:
          temp = out.lower()
          if 'future' in temp or 'wish' in temp or 'will' in temp or "next year" in temp or "petition" in temp or "hope" in temp:
              continue
          if not any([kw in temp for kw in winner_keyword]):
              continue
          numbers = year_pattern.findall(out)
          check = True
          for number in numbers:
              if number != year:
                  check = False
          if check:
              navie = name_pattern.findall(out)
        
              for names in navie:
                  check = nlp(names)
                  sig = False
                  for tok in check.ents:
                    if tok.label_ == 'PERSON':
                        sig = True
                        break
                  
                  if not sig:
                      continue

                  if 'Golden Globe' in names:
                      continue
                  
                  na = names.lower()

                  if any([t in na for t in tem]):
                      continue
                  if na in hosts:
                      hosts[na] += 1
                  else:
                      hosts[na] = 1
      if len(hosts) == 0:
          print(tt, '->', 'None')
          continue
      hosts = sorted(hosts.items(), key = lambda kv:kv[1], reverse= True)
      print(tt, '->', hosts[0])
      hosts = hosts[:5]
      hosts = list(map(list, hosts))
      
getWinners(2013)
    