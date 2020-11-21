# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    jplnasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jplnasa_url + relative_image_path

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)

    facts_df = table[2]
    facts_df.columns = ["Description", "Value"]

    html_table = facts_df.to_html()
    html_table.replace('\n', '')
    
    # Mars 
    listings = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(html_table),
    }

    return listings