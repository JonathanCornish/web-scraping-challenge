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

# MARS NEWS WEBSITE SCRAPE
    # URL for the newspage of NASA's Mars Exploration Project
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # set up splinter & beautiful soup for the Mars News page
    browser = init_browser()
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    time.sleep(1)
    soup = bs(html, "html.parser")

    # Get the latest news title
    news_title = soup.find_all('div', {"class": "content_title"})
    # # show the result
    # news_title[0].text

    # Get the latest paragraph text
    news_para = soup.find_all('div', {"class": "article_teaser_body"})
    # # show the result
    # news_para[0].text

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title[0],
        "news_para": news_para[0]
    }
    # append title and paragraph to mars_dict
    mars_dict['News Title'] = news_title[0]
    mars_dict['News Paragraph'] = news_para[0]

    # Close the browser after scraping
    # browser.quit()

## Website Link for Nasa Mars Picture Scrape ##

    # browser = init_browser()
    base_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(base_url)

    time.sleep(2)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    # browser.click_link_by_partial_text('full_image')
    time.sleep(5)
    # click more info button & get the URL for largesize image, combine with base url
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()
    # # Scrape page into Soup
    html = browser.html
    img_soup = bs(html, "html.parser")
    # find the relative image url
    rel_image = img_soup.select_one("figure.lede a img").get("src")

    # # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    featured_image_url = "https://www.jpl.nasa.gov" + rel_image

    # append url link to mars_dict:
    mars_dict['Mars Feature Image URL'] = featured_image_url

## Nasa Mars Weather Twitter Scrape ##

    # browser = init_browser()
    twit_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twit_url)
    time.sleep(1)
    html = browser.html
    time.sleep(1)
    soup_twit = bs(html, "html.parser")

    # scrape the twitter page, obtain weather info from lastest tweet
    weath_tweet = soup_twit.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # append weather info to mars_dict
    mars_dict['Mars Weather Information'] = weath_tweet
    # print(weath_tweet.text)

## Mars Facts Table Scrape ##

    # browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)
    html = browser.html
    time.sleep(1)
    soup_facts = bs(html, "html.parser")

    # scrape the table using pandas & convert to dataframe using [0] for first item
    tables = pd.read_html(facts_url)[0]
    # tables
    # create the column titles & set the index to Field
    tables.columns = ['Field', 'Value']
    tables = tables.set_index('Field')
    # tables

    html_table = tables.to_html()
    # remove '\n's for aesthetic enhancement:
    html_table = html_table.replace('\n', '')
    mars_dict['Mars Facts Table'] = html_table


# MARS HEMISPHERE PICS

    # browser = init_browser()
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)
    html = browser.html
    time.sleep(1)

    hemis_soup = bs(html, "html.parser")
    hemis = hemis_soup.find_all('div', class_='description')
    # hemis

    # create the dictionary to store the title & image url for each of the four hemispheres:
    hemi_dict = []
    # this is the base url for these hemispheres... I got it by clicking through the website and seeing what 
    # was added onto the href urls to get to the next website link
    base_usgs_url = "https://astrogeology.usgs.gov"

    # create a for loop to loop through each of the hemispheres and grab the titles & image urls
    for hemi in hemis:
        
        # the title is simply at the h3 tag
        title = hemi.find("h3").text
        # the target url link add on is the href tag
        tgt_url = hemi.find('a', class_='itemLink product-item')['href']
        # combine this link with the base url to make the enlarged image url
        img_url_1 = base_usgs_url + tgt_url
        
        # visiting the new url & creating another instance of beautiful soup
        # browser = init_browser()
        browser.visit(img_url_1)
        html = browser.html
        time.sleep(1)
        click_soup = bs(html, "html.parser")
        
        # find the image source
        img = click_soup.find('img', class_="wide-image")["src"]
        img_url = base_usgs_url + img    
        
        # append the hemisphere title + url to the dictionary
        hemi_dict.append({"title": title, "img_url": img_url})

        # append hemi_dict to mars_dict
        mars_dict['Hemisphere URLs'] = hemi_dict

        # add current date & time to mars_dict
        current_dt = dt.datetime.utcnow()
        mars_dict['Date_Time'] = current_dt

    
    final_dict = {
        'News_Headline': mars_dict['News Title'],
        'News_Paragraph': mars_dict['News Paragraph'],
        'Feature_Image_URL': mars_dict['Mars Feature Image URL'],
        'Mars_Current_Weather': mars_dict['Mars Weather Info'],
        'Mars_Facts_Table': mars_dict['Mars Facts Table'],
        'Mars_Hemispheres': mars_dict['Hemisphere URLs'],
        'Date_Time': mars_dict['Date_Time']
    }

    browser.quit()
    return final_dict
        