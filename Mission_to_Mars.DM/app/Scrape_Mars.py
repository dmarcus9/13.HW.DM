from splinter import Browser
from bs4 import BeautifulSoup

# time is a module within python, giving web page/server time to load, 
# called below in step b
import time 

import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

# step a
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_data["title"] = soup.find('div', class_='content_title').a.text 
    mars_data["paragraph"] = soup.find('div', class_='article_teaser_body').get_text()

# step b
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # splinter clicked button for me to get full image
    browser.click_link_by_id('full_image')
    
    time.sleep(2) 

    # grab html after click is important
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # inspected to find appropriate details
    mars_data["featured_image_url"] = 'https://www.jpl.nasa.gov' + soup.find('img', class_='fancybox-image').get('src')

# step c
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_data["mars_weather"] = soup.find('div', class_='js-tweet-text-container').p.text

# step d   pandas (python package) is good for scraping tables
    url = 'http://space-facts.com/mars/'
    # adding "[0]" below makes it a df, not a list
    Mars_Facts_from_table = pd.read_html(url)[0]
    Mars_Facts_from_table.columns = ["characteristics", "value"]
    # "inplace =True" sets the table with the new indices = itself, so it is saved 
    Mars_Facts_from_table.set_index("characteristics", inplace =True) 

    # 2.9 activity...Pandas has a `to_html` method that we can use to generate HTML tables from DataFrames.
    mars_data["html_Mars_Facts_from_table"] = Mars_Facts_from_table.to_html()


# step e   Visit the USGS Astrogeology site:
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
# use the click method from splinter to click links, 
# to obtain high/full resolution images for each of 4 Mar's hemispheres.  
    browser.click_link_by_partial_text('Cerberus')

    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')
# Save both the image url string for the full resolution hemisphere image, 
# and the Hemisphere title containing the hemisphere name. 
    Hemi_image1_Cerberus = hem_soup.find('a', target= "_blank").get('href')
    Hemi_title1_Cerberus = hem_soup.find('h2', class_= "title").text

# to go back a page in browser
    browser.back()
# then click the next image
    browser.click_link_by_partial_text('Schiaparelli')

    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')

    Hemi_image2_Schiaparelli = hem_soup.find('a', target= "_blank").get('href')
    Hemi_title2_Schiaparelli = hem_soup.find('h2', class_= "title").text

    browser.back()
    browser.click_link_by_partial_text('Syrtis')
    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')
    Hemi_image3_Syrtis = hem_soup.find('a', target= "_blank").get('href')
    Hemi_title3_Syrtis = hem_soup.find('h2', class_= "title").text

    browser.back()
    browser.click_link_by_partial_text('Valles')
    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')
    Hemi_image4_Valles = hem_soup.find('a', target= "_blank").get('href')
    Hemi_title4_Valles = hem_soup.find('h2', class_= "title").text

# Use a Python dictionary to store the data using the keys `img_url` and `title`.
    Mars_Hemi_Dict = [
    {"title": Hemi_title1_Cerberus, "img_url": Hemi_image1_Cerberus},
    {"title": Hemi_title2_Schiaparelli, "img_url": Hemi_image2_Schiaparelli},
    {"title": Hemi_title3_Syrtis, "img_url": Hemi_image3_Syrtis},
    {"title": Hemi_title4_Valles, "img_url": Hemi_image4_Valles}
    ] 
    mars_data["Mars_Hemi_Dict"] = Mars_Hemi_Dict 

# printing to terminal console
    print(mars_data)

# returns it to scraped_data in app.py
    return mars_data
