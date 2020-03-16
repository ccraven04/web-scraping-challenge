# Import Dependencies
from IPython.display import Image
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time
import shutil
import re


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():

    # Visit URL for NASA News


    nasa_news = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_news)


    # Create the NASA soup - inspect for classes

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    type(soup)


    # save the most recent article, title and date

    article = soup.find("div", class_="list_text")
    news_date = article.find("div", class_="list_date").text
    news_title = article.find("div", class_="content_title").text
    news_paragraph = article.find("div", class_="article_teaser_body").text
    print()
    print()
    print(f"The article date is:   {news_date}")
    print()
    print(f"The article title is:   {news_title}")
    print()
    print(f"The article descrition paragraph is:   {news_paragraph}")
    print()


    # Image URL

    mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image)


    # Image Soup

    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')


    # Find image using soup

    image = img_soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image
    featured_image_url


    response = requests.get(featured_image_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


    # image URL
    print(f"The image url is: {featured_image_url}")

    # Mars image
    Image(url='img.jpg')


    # weather URL

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)


    # Weather Soup

    w_html = browser.html
    weather_soup = BeautifulSoup(w_html, 'html.parser')
    print(weather_soup.prettify())


    r = requests.get(weather_url)
    html = r.text
    soup = BeautifulSoup(html)
    soup


    for result in soup.find_all('p', class_={re.compile(r'^tweet')}):
        mars_weather = result.get_text()
        if 'InSight sol' in mars_weather:
            print(mars_weather)
            break


    # Mars Facts URL for table

    facts_url = "https://space-facts.com/mars/"

    facts = pd.read_html(facts_url)

    facts



    mars_facts = facts[0]
    mars_facts.columns = ["Element", "Value"]
    mars_facts


    mars_facts_html = mars_facts.to_html(header=False, index=False)
    print(mars_facts_html)


    # ### Mars Hemispheres

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)


    # Hemisphere dictionaries

    mars_hemisphere = []


    for i in range(4):
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2", class_="title").text
        img_url = 'https://astrogeology.usgs.gov' + partial
        dictionary = {"title": img_title, "img_url": img_url}
        mars_hemisphere.append(dictionary)
        browser.back()


    mars_hemisphere

