from processTweets import process_tweet
from data import handle_Data
import spacy
from spacy.symbols import nsubj, dobj
import re
# nlp = spacy.load('en_core_web_sm')
# check = nlp('Daniel Day')
# sig = False
# for tok in check.ents:
#     if tok.label_ == 'PERSON':
#         print(tok.text)

def getNominees(year):
    name_pattern = re.compile(r'[A-Z]\w*\s[A-Z]\w*')
    year_pattern = re.compile(r'\d{4}')
    
    awards2nominee = {}
    awards2tweets, awards_list, Newname2name = process_tweet(year)

    for tt in awards2tweets:
     nominees = {}
     a_real_name = Newname2name[tt]
     result = awards2tweets[tt]
     nom_keyword = ['win', 'won', 'hope', 'wish', 'rob', 'robbed']
     tem = ['@', 'best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance', 'series', 'tv', 'mini', 'golden globe', 'song']
     tem1 = ['@', 'best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance', 'series', 'tv', 'mini', 'golden globe', 'song', 'and']
     nlp = spacy.load('en_core_web_sm')
     
     if ('actor' not in tt) and ('actress' not in tt) and ('cecil' not in tt) and ('director' not in tt):
         for out in result:
   
             temp = out.lower()
             if not any([kw in temp for kw in nom_keyword]):
              continue
             o = nlp(out)

             foundWinner = False
             for tok in o.ents:
                work_name = tok.text.lower()
                if any([t in work_name for t in tem]):
                    continue
                if tok.label_ == 'WORK_OF_ART':
                  work_name = re.sub(r'[^\w\s]', '', work_name)
                  foundWinner = True
                #   if (work_name in winnerd[a_real_name]) or (winnerd[a_real_name] in work_name):
                #       continue
                #   signal = False
                #   for i in presenterd[a_real_name]:
                #     if (work_name in i) or (i in work_name):
                #       signal = True
                #       break
                #   if signal:
                #       continue
                  if work_name in nominees:
                      nominees[work_name] += 1
                  else:
                      nominees[work_name] = 1
             if not foundWinner:
                 for possible_subject in nlp(out):
                    if possible_subject.dep == nsubj and (str(possible_subject.head) == 'won' or str(possible_subject.head) == 'wins' or str(possible_subject.head) == 'win' or str(possible_subject.head) == 'takes' or str(possible_subject.head) == 'took'):
                        for chunk in nlp(out).noun_chunks:
                            sig = False
                            for ent in nlp(chunk.text).ents:
                                if ent.label_ == 'PERSON':
                                    sig = True
                                    break
                            if sig:
                                continue
                            # if (chunk.text.lower() in winnerd[a_real_name]) or (winnerd[a_real_name] in chunk.text.lower()):
                            #     continue
                            # signal = False
                            # for i in presenterd[a_real_name]:
                            #     if (chunk.text.lower() in i) or (i in chunk.text.lower()):
                            #         signal = True
                            #         break
                            # if signal:
                            #     continue
                            if any([t in chunk.text.lower() for t in tem]):
                                continue
                            if str(possible_subject).lower() in chunk.text.lower():
                                foundWinner = True
                                if chunk.text.lower() in nominees:
                                    nominees[chunk.text.lower()] += 1
                                else:
                                    nominees[chunk.text.lower()] = 1
                    elif possible_subject.dep == dobj and str(possible_subject.head) == 'to':
                        for chunk in nlp(out).noun_chunks:
                            sig = False
                            for ent in nlp(chunk.text).ents:
                                if ent.label_ == 'PERSON':
                                    sig = True
                                    break
                            if sig:
                                continue
                            # if (chunk.text.lower() in winnerd[a_real_name]) or (winnerd[a_real_name] in chunk.text.lower()):
                            #     continue
                            # signal = False
                            # for i in presenterd[a_real_name]:
                            #     if (chunk.text.lower() in i) or (i in chunk.text.lower()):
                            #         signal = True
                            #         break
                            # if signal:
                            #     continue
                            if any([t in chunk.text.lower() for t in tem]):
                                continue
                            if str(possible_subject).lower() in chunk.text.lower():
                                foundWinner = True
                                if chunk.text.lower() in nominees:
                                    nominees[chunk.text.lower()] += 1
                                else:
                                    nominees[chunk.text.lower()] = 1
            #  if not foundWinner:
            #      possible_names = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)', out)
            #      for name in possible_names:
            #       name = name.lower()
            #       if name in winners:
            #           winners[name] += 1
            #       else:
            #           winners[name] = 1    
     else:
  

         
      for out in result:
          temp = out.lower()
          if not any([kw in temp for kw in nom_keyword]):
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

                  if any([t in na for t in tem1]):
                      continue
                #   if (na in winnerd[a_real_name]) or (winnerd[a_real_name] in na):
                #       continue
                #   signal = False
                #   for i in presenterd[a_real_name]:
                #     if (na in i) or (i in na):
                #             signal = True
                #             break
                #   if signal:
                #             continue
                  if na in nominees:
                      nominees[na] += 1
                  else:
                      nominees[na] = 1
     if len(nominees) == 0:
        # print(tt, '->', 'None')
        newAN = Newname2name[tt]
        awards2nominee[newAN] = []       
        continue
     nominees = sorted(nominees.items(), key = lambda kv:kv[1], reverse= True)
     newAN = Newname2name[tt]
     num = 4
     if len(nominees) < 4:
         num = len(nominees)
     tempor = []
     
     for i in range(num):
            tempor.append(nominees[i][0])
            print(nominees[i][0])
     awards2nominee[newAN] = tempor
    # print(awards2winner)
    return awards2nominee 
    #  print(tt, '->',winners[0])
    #  if len(winners) >= 2:
    #     print(tt, '->',winners[1])
