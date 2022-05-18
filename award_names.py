
from ast import Num
from lib2to3.pgen2 import token
from data import handle_Data
import spacy
import re

stop_word_exclusion = ['by', 'an', 'a', 'or', 'in', 'made']
punt_exclusion = [',']
a_list = []
# nlp = spacy.load('en_core_web_sm')
# a = nlp("for")
# for tok in a:
#     print(tok.text, '->', tok.is_stop)

def find_award_names(year):
    # load english language model
    if year == 2013 or year == 2015:
        num = 28
    else:
        num = 28
    nlp = spacy.load('en_core_web_sm')
    nlp.Defaults.stop_words |= {'goes', 'golden'}
    added_stop = {'-', 'win', 'won'}
    pattern = re.compile(r'best', re.I)
    result = handle_Data(year)
    awards_dict = {}
    for out in result:
        match_ob = re.search(pattern, out)
        if match_ob:
            start_pos = match_ob.start()
            tem = out[start_pos:]
            tem = tem.lower()
            tem = nlp(tem)
            res = []
            for tok in tem:               
                if (tok.is_stop and tok.text not in stop_word_exclusion) or (tok.is_punct and tok.text not in punt_exclusion):
                    break

                res.append(tok.text)
            
            if len(res) <= 3:
                continue
            res = ' '.join(res)
            if res in awards_dict:
                awards_dict[res] += 1
            else:
                awards_dict[res] = 1
    awards_dict = sorted(awards_dict.items(), key = lambda kv:kv[1], reverse= True)    
    if len(awards_dict) < num:
        num = len(awards_dict)
    for i in range(num):
        a_list.append(awards_dict[i])
    return a_list
  
find_award_names(2013)