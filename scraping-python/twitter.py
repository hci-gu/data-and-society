import json
import time
import requests
from bs4 import BeautifulSoup

base_url = 'https://twitter.com'
path = '/weirddalle'
pages = 10


def get_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_tweets(url):
    print('start: ' + url)
    data = []
    soup = get_html(url)

    tweets = soup.find_all("article")
    print(tweets)
    for tweet in tweets:
        print(tweet)
        # data.append({
        # })
    return data


data = []
url = base_url + path
data += get_tweets(url)
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
