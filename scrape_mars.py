from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
     
def get_nasa_mars_news(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.select_one("ul.item_list li.slide")
    news_title_text = news_title.find("div", class_= "content_title").get_text()
    news_teaser = news_title.find("div", class_="article_teaser_body").get_text()
    
    return {
        "news_title": news_title_text,
        "news_teaser": news_teaser
    }

def get_mars_image_url(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    mars_image = browser.find_by_id("full_image")
    mars_image.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info = browser.links.find_by_partial_text("more info")
    more_info.click()

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    relative_url = "https://www.jpl.nasa.gov"
    image_path = soup.select_one("figure.lede a").get("href")
    featured_image_url = relative_url + image_path
    return featured_image_url

def get_mars_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find(name="span", text = re.compile(r"(InSight sol )\d*[\w\W]{1,}")).text
    return mars_weather

def get_mars_facts(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    tables = pd.read_html(url)
    facts = tables[0]
    facts.columns = ['Characteristics', 'Values']
    facts.set_index('Characteristics', inplace=True)
    facts_html = facts.to_html()
    facts_html.replace("\n", "")
    return facts_html

def get_mars_hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    hemisphere_image_urls = []

    for i in range(4):

        hemisphere_link = browser.find_by_css("div.description a")[i]
        hemisphere_link.click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        hemisphere_image_url = {}
    
        hemisphere_image_url["title"] = soup.find("h2").text
        hemisphere_image_url["image_url"] = soup.find("a", text = "Sample").get("href")
        hemisphere_image_urls.append(hemisphere_image_url)
    
        browser.back()

    return hemisphere_image_urls

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    mars_news = get_nasa_mars_news(browser)
    mars_image_url = get_mars_image_url(browser)
    mars_weather = get_mars_weather(browser)
    mars_facts = get_mars_facts(browser)
    mars_hemispheres = get_mars_hemispheres(browser)

    # browser.quit()
    
    mars_scraped = {
        "mars_news": mars_news,
        "mars_image_url": mars_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "mars_hemispheres": mars_hemispheres
    }
    
    return mars_scraped