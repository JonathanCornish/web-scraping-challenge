from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time
import datetime as dt
import pandas as pd
import requests
from pprint import pprint

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    # empty dictionary for holding all scraped data, allows for MongoDB storage
    mars_dict = dict()
    browser = init_browser()

#     URL for the newspage of NASA's Mars Exploration Project
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

#     time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news title
    news_title = soup.find_all('div', {"class": "content_title"})
    news_title[0].text

    # Get the latest paragraph text
    news_para = soup.find_all('div', {"class": "article_teaser_body"})
    news_para[0].text

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title[0],
        "news_para": news_para[0]
    }

    # Close the browser after scraping
#     browser.quit()

    # Return results
    return mars_data
    print(mars_data)
#     return news_title

## Nasa Mars News Website Scrape ##

    browser = init_browser()

    #     URL for the newspage of NASA's Mars Exploration Project
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news title
    news_title = soup.find_all('div', {"class": "content_title"})
    news_title[0].text

    # Get the latest paragraph text
    news_para = soup.find_all('div', {"class": "article_teaser_body"})
    news_para[0].text

    print(news_title[0].text)
    print(news_para[0].text)

    ## Website Link for Nasa Mars Picture Scrape ##

    browser = init_browser()
    base_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(base_url)

    time.sleep(1)
    full_image = browser.find_by_id("full_image")

    full_image.click()
    time.sleep(5)
    more_info_button = browser.find_link_by_partial_text("more info")

    more_info_button.click()

    # # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    rel_image = soup.select_one("figure.lede a img").get("src")
    # print(rel_image)
    #page > section.content_page.module > div > article > figure > a > img

    # # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    featured_image_url = "https://www.jpl.nasa.gov" + rel_image
    print(featured_image_url)

    ## Nasa Mars Weather Twitter Scrape ##

    browser = init_browser()
    twit_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twit_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    weath_tweet = soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    print(weath_tweet.text)

    ## Mars Facts Table Scrape ##

    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    # mars_fact_table = soup.find('table', {"id": "tablepress-p-mars"})

    # print(mars_fact_table.text)
    tables = pd.read_html(facts_url)[0]
    # tables

    tables.columns = ['Field', 'Value']
    tables = tables.set_index('Field')
    # tables

    html_table = tables.to_html()
    # html_table

    # remove '\n's for aesthetic enhancement:

    html_table = html_table.replace('\n', '')
    # html_table

    browser = init_browser()
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)

    time.sleep(1)

    hemis_soup = bs(html, "html.parser")

    hemis = hemis_soup.find_all('div', class_='description')
    hemis

    # create the dictionary to store the title & image url for each of the four hemispheres:
    hemi_dict = []
    # this is the base url for these hemispheres... I got it by clicking through the website and seeing what 
    # was added onto the href urls to get to the next website link
    base_usgs_url = "https://astrogeology.usgs.gov"

    # create a for loop to loop through each of the hemispheres and grab the titles & image urls
    for hemi in hemis:
        
        #     the title is simply at the h3 tag
        title = hemi.find("h3").text
        
        #     the target url link add on is the href tag
        tgt_url = hemi.find('a', class_='itemLink product-item')['href']

        #     combine this link with the base url to make the enlarged image url
        img_url_1 = base_usgs_url + tgt_url
        
        #     visiting the new url & creating another instance of beautiful soup
        browser = init_browser()
        browser.visit(img_url_1)
        html = browser.html
        time.sleep(1)
        click_soup = bs(html, "html.parser")
        
        #     find the image    
        img = click_soup.find('img', class_="wide-image")["src"]
        img_url = base_usgs_url + img    
        
        #     append the hemisphere title + url to the dictionary
        hemi_dict.append({"title": title, "img_url": img_url})
        
    # print(hemi_dict)