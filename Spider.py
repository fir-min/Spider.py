import requests
import time, datetime
from bs4 import BeautifulSoup
try:
    import cPickle as pickle
except:
    import pickle



unique_links = {}
crawl_result = {}

def crawl(url_list):
    for url in url_list:
        unique_links[url] = 'None'
        extract_links_from_url(url)

    for url in unique_links.keys():
        try:
            request = requests.get(url)
            content = BeautifulSoup(request.content, 'html.parser')
            temp_dict = {}
            temp_dict['title'] = content.title
            temp_dict['text'] = content.get_text() #+ ' ' + content.get('title')
            temp_dict['all'] = '{0} {1}'.format(content.title, content.get('text'))
            crawl_result[url] = temp_dict
            #print('working...')

        except:
            #print('oops')
            continue


def extract_links_from_url(url):

    request = requests.get(url)

    content = BeautifulSoup(request.content, 'html.parser')


    for link in content.find_all('a', limit=2):
        #dict['count'] = dict['count'] + 1
        href = link.get('href')
        #print(dict['count'])
        if not unique_links.has_key(href):
            unique_links[href] = link.string

# mode: 0 - search in title, 1 - body, 2 - both
def search(key_word, mode = 0):
    result = []
    for r in crawl_result.keys():
        content = [crawl_result[r]['title'], crawl_result[r]['text'], crawl_result[r]['all']]
        text = content[mode]
        try:
            if key_word in text:
                result.append(r)
                #print('searching...')
        except:
            continue

    return result

def print_links():
    for link in unique_links.keys():
        print(link)

def search_and_print_result(key_word, mode = 0):
    result = search(key_word, mode)
    for x in result:
        print(x)

'''
def load_crawl_data(filename):
    with open(filename, 'rb') as fp:
        crawl_result = pickle.load(fp)

def save_crawl_data(folder_path):
    filename = '{0}.spider'.format(datetime.datetime.now())
    with open(filename, 'wb') as fp:
        pickle.dump(crawl_result, fp)

'''




#save_crawl_data('/Users/fsa/Documents/Py/')


crawl(['https://www.tumblr.com/tagged/art'])
search_and_print_result("tumblr", 2)