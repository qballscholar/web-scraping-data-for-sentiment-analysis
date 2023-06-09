#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import os
import sys
import time
import random
# URL of the public LinkedIn profile you want to scrape
URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
page = requests.get(URL, headers=HEADERS)


def time_delay():
    time.sleep(random.randint(2, 5))


if page.status_code != 200:
    print("Unable to find URL")

# Send a GET request to the URL and parse the HTML content using BeautifulSoup
else:
    soup = BeautifulSoup(page.content, "html.parser")
    movie_column = soup.find_all('tbody')
    titles = soup.find_all('td', {'class': 'titleColumn'})
    base_url = "https://www.imdb.com"
    for title in titles:
        try:
            # Get title only by pulling out the a tag and create a file name in a directory called Reviews
            f = open("Reviews/" + title.a.text, 'w', encoding='utf-8')
        except FileNotFoundError:
            os.makedirs("Reviews")
            f = open("Reviews/" + title.a.text, 'w', encoding='utf-8')
# Directory not found, create Directory first ## Send a GET request to the URL and parse the HTML content using BeautifulSoup
        movie_details_url = "{}{}".format(base_url, title.a['href'])
        movie_page = requests.get(movie_details_url, headers=HEADERS)
        soup = BeautifulSoup(movie_page.content, "html.parser")
# Find the User reviews href
        ipc_link = soup.find_all(
            'a', {'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})
        review_link = None
        for r in ipc_link:
            if r.text == "User reviews":
                review_link = r['href']
# Title sub needs to be stripped out to get FQDN of the Reviews page
        title_sub = "/".join(title.a['href'].split('/',3)[:3])
        print(title_sub)

# Navigate to Movie title's review page
        if review_link is not None:
            all_reviews_page = requests.get("{}{}/{}".format(base_url, title_sub, review_link))
            soup = BeautifulSoup(all_reviews_page.content, "html.parser")
            reviews = soup.find_all('div', {'class': 'text show-more__control'})

            for review in reviews:
                comment = review.text
                f.write(review.text.strip() + '\n')
        
        f.close()