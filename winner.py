


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
 
def getWinners(year):
    name_pattern = re.compile(r'[A-Z]\w*\s[A-Z]\w*')
    year_pattern = re.compile(r'\d{4}')
    
    awards2winner = {}
    awards2tweets, awards_list, Newname2name = process_tweet(year)

    for tt in awards2tweets:
     winners = {}
     result = awards2tweets[tt]
     winner_keyword = ['win', 'won', 'goes to', 'go to', 'congrates', 'congratulations', 'congratulate', '-', 'for']
     tem = ['@', 'best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance', 'series', 'tv', 'mini', 'golden globe', 'song']
     tem1 = ['@', 'best', 'director', 'motion', 'picture', 'actor', 'actress', 'supporting', 'comedy', 'musical', 'mini-series', 'screenplay', 'performance', 'series', 'tv', 'mini', 'golden globe', 'song', 'and']
     nlp = spacy.load('en_core_web_sm')
     
     if ('actor' not in tt) and ('actress' not in tt) and ('cecil' not in tt) and ('director' not in tt):
         for out in result:
   
             temp = out.lower()
             if 'future' in temp or 'wish' in temp or 'will' in temp or "next year" in temp or "petition" in temp or "hope" in temp:
              continue
             if not any([kw in temp for kw in winner_keyword]):
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
                  if work_name in winners:
                      winners[work_name] += 1
                  else:
                      winners[work_name] = 1
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
                            if any([t in chunk.text.lower() for t in tem]):
                                continue
                            if str(possible_subject).lower() in chunk.text.lower():
                                foundWinner = True
                                if chunk.text.lower() in winners:
                                    winners[chunk.text.lower()] += 1
                                else:
                                    winners[chunk.text.lower()] = 1
                    elif possible_subject.dep == dobj and str(possible_subject.head) == 'to':
                        for chunk in nlp(out).noun_chunks:
                            sig = False
                            for ent in nlp(chunk.text).ents:
                                if ent.label_ == 'PERSON':
                                    sig = True
                                    break
                            if sig:
                                continue
                            if any([t in chunk.text.lower() for t in tem]):
                                continue
                            if str(possible_subject).lower() in chunk.text.lower():
                                foundWinner = True
                                if chunk.text.lower() in winners:
                                    winners[chunk.text.lower()] += 1
                                else:
                                    winners[chunk.text.lower()] = 1
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

                  if any([t in na for t in tem1]):
                      continue
                  if na in winners:
                      winners[na] += 1
                  else:
                      winners[na] = 1
     if len(winners) == 0:
        # print(tt, '->', 'None')
        newAN = Newname2name[tt]
        awards2winner[newAN] = 'None'       
        continue
     winners = sorted(winners.items(), key = lambda kv:kv[1], reverse= True)
     newAN = Newname2name[tt]
     awards2winner[newAN] = winners[0][0]
    print(awards2winner)
    return awards2winner
    #  print(tt, '->',winners[0])
    #  if len(winners) >= 2:
    #     print(tt, '->',winners[1])
getWinners(2013)
