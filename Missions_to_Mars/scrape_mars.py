# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

    # Initialize browser 
    browser = init_browser()

    #browser.is_element_present_by_css("div.content_title", wait_time=1)

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    return mars_info

        #browser.quit()


#NASA MARS IMAGES
def scrape_mars_image():

    # Initialize browser 
    browser = init_browser()

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)


    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, "html.parser")

    # Retrieve background-image url from style tag 
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = "https://www.jpl.nasa.gov"

    # Concatenate website url with scrapped route
    image_url = main_url + image_url

    # Display full link to featured image
    return image_url

#NASA MARS FACTS
def scrape_mars_facts():
    # Initialize browser 
    browser = init_browser()

    url = "https://space-facts.com/mars/"

    browser.visit(url)

    # Use Pandas to "read_html" to parse the URL

    tables = pd.read_html(url)

    #tables[0]
    #Find Mars Facts DataFrame in the lists of DataFrames
    
    df= tables[0]
    #Assign the columns
    
    df.columns = ['Description', 'Value']
    
    
    #Save html to folder and show as html table string
    mars_df = df.to_html(classes = 'table table-striped')
    return mars_df


#NASA MARS WEATHER 
def scrape_mars_weather():
    # Initialize browser 
    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(weather_url)

    time.sleep(1)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        mars_weather = tweet.find('p').text
        # if 'Sol' and 'pressure' in mars_weather:
        #     print(mars_weather)
        #     break
        # else: 
        #     pass
    mars_weather= "33d"
    return mars_weather


#NASA MARS HEMISPHERES
def scrape_mars_hemispheres ():
    # Initialize browser 
    browser = init_browser()
    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(1)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
    # Store title
        title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    return mars_hemispheres