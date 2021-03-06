'''Version 0.35'''

import json
from Nominee import getNominees
from winner import getWinners
from hosts import findhosts
from sentiment import getSentiment
from bestdress import findbestandwrostdressed
from award_names import find_award_names
from presenter import find_presenter

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = findhosts(year)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = find_award_names(year)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here

    nominees = getNominees(year)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = getWinners(year)
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return find_presenter(year)

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # years = [2013, 2015]
    years = [2013]
    #Finalresult contain the final answer for 2013 and 2015
    Finalresult = dict()

    for year in years:
        hosts = get_hosts(year)
        print("Finish Hosts")
        awards = get_awards(year)
        print("Finish awards")
        winners = get_winner(year)
        print("Finish winners")
        nominees = get_nominees(year)
        print("Finish nominees")
        presenters = get_presenters(year)
        print("Finish presenters")
        sentiments = getSentiment(year)
        print("Finish sents")
        dreesed = findbestandwrostdressed(year)
        print("Finish dresss")

        result = dict()
        result["hosts"] = hosts
        result["award_data"] = {}
        #print output with humanread format with extra goals
        print("Host: ", end =" ")
        print(hosts)
        print("Best Dressed: ", end =" ")
        print(dreesed[0])
        print("Worst Dressed: ", end =" ")
        print(dreesed[1])
        for award in OFFICIAL_AWARDS_1315:
            print('\n')
            print(award)
            result["award_data"][award] = dict()
            result["award_data"][award]["nominees"] = nominees[award]
            result["award_data"][award]["presenters"] = presenters[award]
            result["award_data"][award]["winner"] = winners[award]
            
            print("nominees: ", end =" ")
            print(nominees[award])
            print("presenters: ", end =" ")
            print(presenters[award])
            print("winner: ", end =" ")
            print(winners[award])
            print("sentiment: ", end =" ")
            print(sentiments[award])
        Finalresult[year] = result

    #save json format result to file   
    out_file = open("result.json", "w")
  
    json.dump(Finalresult, out_file)
  
    out_file.close()
        




    return

if __name__ == '__main__':
    main()

