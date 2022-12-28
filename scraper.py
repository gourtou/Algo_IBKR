from bs4 import BeautifulSoup
import requests
import time
import datetime
from random import randint

# Global variables
POSITIVE = ['exceeds', 'beats', 'apple', 'expectations']
NEGATIVE = ['drops', 'down']
TEXTS = []       # news headlines
CYCLE = 4


def search_economist():
    page_link = 'https://www.economist.com/'
    page_response = requests.get(page_link, timeout=30)
    page_content = BeautifulSoup(page_response.content, 'html.parser')

    for link in page_content.find_all('span', class_="teaser__headline", limit=3):
        if link.text not in TEXTS:
            print(link.text)    # Prints the title so we can verify correct operation
            TEXTS.append(link.text)     # Appends the headline to our main array
            headline_holder.append(link.text)
    print("Economist Done")
    time.sleep(5)   # required by the Economist in robots.txt


def search_seekingalpha():
    page_link = 'https://seekingalpha.com/market-news/all'
    page_response = requests.get(page_link, timeout=30)
    page_content = BeautifulSoup(page_response.content, 'html.parser')

    for link in page_content.find_all('div', class_="media-body", limit=3):
        if link.div.a.text not in TEXTS:
            print(link.text)    # Prints the title so we can verify correct operation
            TEXTS.append(link.div.a.text)     # Appends the headline to our main array
            headline_holder.append(link.div.a.text)
    print("Seeking Alpha Done")
    time.sleep(1)


def search_cnn():
    page_link = 'https://www.cnn.com/specials/last-50-stories'  # Page Url to point request where to crawl
    page_response = requests.get(page_link, timeout=30)  # Get request to ask for page content
    page_content = BeautifulSoup(page_response.content, "html.parser")  # Ask Beautiful soup to parse for content

    for link in page_content.find_all("span", class_="cd__headline-text", limit=3):  # Finds all the spans with the class cd__headline-text
        if link.text not in TEXTS:
            # print(link.text)	# Prints the title so we can verify correct operation
            TEXTS.append(link.text)  # Appends the headline to our main array
            headline_holder.append(link.text)
    print("CNN Done")
    time.sleep(1)


def search_reuters():
    page_link = 'https://www.reuters.com/'  # Page Url to point request where to crawl
    page_response = requests.get(page_link, timeout=30)  # Get request to ask for page content
    page_content = BeautifulSoup(page_response.content,"html.parser")  # Ask Beautiful soup to parse for content

    for link in page_content.find_all("h3", class_="article-heading", limit=3):  # Finds h3's with the class article-heading
        if link.text not in TEXTS:
            # print(link.text)	# Prints the title so we can verify correct operation
            TEXTS.append(link.text)  # Appends the headline to our main array
            headline_holder.append(link.text)
    print("Reuters Done")
    time.sleep(1)


def headline_analysis(headline):
    words = headline.split()        # split to words
    match_score = 0
    for word in words:
        if word.lower() in POSITIVE:
            match_score += 1

    if match_score >= 3:
        result = 'trigger_long_execution'
    elif match_score <= -3:
        result = 'trigger_short_execution'
    else:
        result = 'no_change'
    return result

if __name__ == '__main__':

    cycle_count = 0
    headline_holder = []

    while True:
        search_economist()
        search_seekingalpha()
        search_cnn()
        search_reuters()
        cycle_count += 1
        print('Search finished, cycle', cycle_count)
        if cycle_count == CYCLE:
            headline_holder.append('Apple exceeds expectations')

        for entry in headline_holder:
            print(entry)
            headline_analysis(entry)

        headline_holder = []
        time.sleep(randint(1, 5))
