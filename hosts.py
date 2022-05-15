from data import handle_Data
import spacy
import re

def findhosts(year):
    # load english language model
    nlp = spacy.load('en_core_web_sm')
    pattern = re.compile(r'host', re.I)
    name_pattern = re.compile(r'[A-Z][a-z]* [A-Z][a-z]*')
    year_pattern = re.compile(r'\d{4}')
    result = handle_Data(year)
    
    hosts = {}
    total = 0
    for out in result:
        temp = out.lower()
        if 'future' in temp or 'wish' in temp or 'will' in temp or "next year" in temp or "petition" in temp:
            continue
        if (re.search(pattern, out)):
            numbers = year_pattern.findall(out)
            check = True
            for number in numbers:
                if number != year:
                    check = False
            if check:
                navie = name_pattern.findall(out)
                for names in navie:
                    if 'Golden Globe' in names:
                        continue
                    na = names.lower()
                    if na in hosts:
                        hosts[na] += 1
                    else:
                        hosts[na] = 1
    hosts = sorted(hosts.items(), key = lambda kv:kv[1], reverse= True)
    print(hosts)
    hosts = hosts[:5]
    hosts = list(map(list, hosts))
    """
    for x in range(5):
        if ' ' not in hosts[x][0]:
            for y in range(5):
                if x != y and hosts[x][0] in hosts[y][0]:
                    hosts[y][1] += hosts[x][1]
                    hosts[x][1] = 0
    hosts = sorted(hosts, key = lambda kv:kv[1], reverse= True)
    hosts = hosts[:2]
    print(hosts)
    """


findhosts(2015)


