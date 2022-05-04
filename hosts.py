from data import handle_Data
import spacy
import re

def findhosts(year):
    # load english language model
    nlp = spacy.load('en_core_web_sm')
    pattern = re.compile(r'host', re.I)
    result = handle_Data(year)
    hosts = {}
    for out in result:
        if re.search(pattern, out):
            tok = nlp(out)
            for names in tok.ents: 
                if names.label_ == 'PERSON':
                    if names.text in hosts:
                        hosts[names.text] += 1
                    else:
                        hosts[names.text] = 1
    print(hosts)

findhosts(2013)
#a
