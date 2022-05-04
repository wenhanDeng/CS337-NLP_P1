
from lib2to3.pgen2 import token
from data import handle_Data
import spacy
import re

stop_word_exclusion = ['by', 'an', 'a', 'or', 'in', 'made', 'for']
punt_exclusion = ['-', ',']

# nlp = spacy.load('en_core_web_sm')
# a = nlp("for")
# for tok in a:
#     print(tok.text, '->', tok.is_stop)

def find_award_names(year):
    # load english language model
    nlp = spacy.load('en_core_web_sm')
    nlp.Defaults.stop_words |= {'goes', 'golden'}
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
                if '-' in res and tok.text == '-':
                    break
                if tok.text == 'tv':
                    res.append('television')
                    continue
                if tok.ent_type_ == 'PERSON':
                    if len(res) != 0 and  res[-1] == '-':
                        res.pop()
                    break
                res.append(tok.text)
            
            if len(res) <= 3:
                continue
            res = ' '.join(res)
            if res in awards_dict:
                awards_dict[res] += 1
            else:
                awards_dict[res] = 1
    for i in awards_dict:
        if awards_dict[i] >= 10:
            print(i, awards_dict[i])
 
  
find_award_names(2013)