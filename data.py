#Handle json files
import json


def handle_Data(year) :
    # JSON file
    file = f'gg{year}.json'
    f = open (file)
    # Save the posts in dictonary
    data = json.load(f)
    #list that store text data
    posts = []
    for out in data:
        temp = out['text']
    #get rid of tags
        temp = temp.split('#')[0]
        posts.append(temp)
    return posts
