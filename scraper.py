from bs4 import BeautifulSoup
import requests
import time

# Global variables
TEXTS = []      # news headlines
CYCLE = 0       # frequency of server requests


def search_economist():
    page_link = 'https://www.economist.com/'
    page_response = requests.get(page_link, timeout=30)
    page_content = BeautifulSoup(page_response.content, 'html.parser')
