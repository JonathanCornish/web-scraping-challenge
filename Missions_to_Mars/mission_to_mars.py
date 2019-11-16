from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
#     url = "https://visitcostarica.herokuapp.com/"
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news title
    news_title = soup.find('div', id='weather')
    # news_title = soup.find_all('div', class='weather')

    # Get the latest paragraph text
    news_para = avg_temps.find_all('strong')[0].text

    # BONUS: Find the src for the mars image
#     relative_image_path = soup.find_all('img')[2]["src"]
#     sloth_img = url + relative_image_path

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_para": news_para
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data