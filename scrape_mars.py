# Setup Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_fourth_planet():

    # ### Mission to Mars - code is largely from Jupyter Notebook


    # Get data from the NASA Mars News website
    # Beware, as the martians have hacked the website!!!
    # The HTML that is returned does not necessarily match what is shown on the website
    # I will use what the martians give me, thus it might not match what's on the website for humans.

    # The url for the website
    url = "https://mars.nasa.gov/news"
#    print (f'Getting data from {url}...' )

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Initialize a mars_info list
    mars_news = []

    # Stop after the third news headline is picked off
    n_slides = 0

    # The desired information is in the "Div class=slide" tags
    for slide in soup.find_all('div', class_='slide'):
        
        # Pick off the slide title
        slide_title = slide.find("div", class_="content_title").a.text.strip()
        
        # Pick off the teaser paragraph
        teaser = slide.find('div', class_="rollover_description_inner").text.strip()

        # Pick off the URL, it is in the first "a" tag
        slide_urls = slide.find_all('a')
        slide_url = slide_urls[0]["href"]
        base_url = "https://mars.nasa.gov/news"
        news_story_url = base_url + slide_url

        # Append to the list
        mars_news.append({'teaser':teaser, 'title':slide_title, 'url':news_story_url})

        # Count the number of slides, stop if this is the third one
        n_slides += 1
        if (n_slides==3):
            break

    # 'mars_info' will be the Python Dictionary that contains all the information scraped from the web.
    # The first entry has the key "Headlines", and the value is the list of dictionaries of titles & teasers
    mars_info = {'Headlines':mars_news}


    # Get the Featured Image from the JPL Mars Space Images website
    # The url for the website
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#    print (f'Getting data from {url}...' )

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # From the "article" tag with the "carousel_item" class, pick off the "style"
    style_detail = soup.find('article', class_='carousel_item')['style']

    # Now, split the text of the "style" by the single quote "'".  The second item (i.e. #1), is the detail of the URL
    detail_url = style_detail.split("'")[1]

    # Put the base URL in front of the detailed URL
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + detail_url

    # Add this to the 'mars_info' dictionary
    mars_info.update({'Featured_Image':featured_image_url})

    # Get the Current Mars Weather from Twitter
    # The url for the website
    url = "https://twitter.com/marswxreport?lang=en"
#    print (f'Getting data from {url}...' )

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # The HTML code for one tweet
    soup.find('li', class_='js-stream-item stream-item stream-item')

    # Loop through all the tweets that were found (Twitter returns 20)
    # The current weather is the first one that has the username "Mars Weather"
    # and where the first word is "InSight"

    mars_weather = "Could not find it, as there are too many non-weather tweets right now"

    for tweet in soup.find_all('li', class_='js-stream-item stream-item stream-item'):
        username = tweet.find('strong', class_='fullname').text
        too_much_tweet_text = tweet.find('p', class_="TweetTextSize").text
        
        try:
            link_text = tweet.find('a', class_='twitter-timeline-link').text
        except Exception as e:
            link_text = ""
            
        tweet_text = too_much_tweet_text.replace(link_text,"")
        first_word = tweet_text.split(' ')[0]
        if (username == "Mars Weather") and (first_word == "InSight"):
            mars_weather = tweet_text
            break
            
    # Add this to the 'mars_info' dictionary
    mars_info.update({'Weather':mars_weather})

    # Get some facts about Mars
    # The url for the website
    url = "https://space-facts.com/mars/"
#    print (f'Getting data from {url}...' )

    # Use Pandas "read_html" to find all the tables on the webpage
    tables = pd.read_html(url)

    # We are only interested in the third table
    mars_table = tables[2]

    # Add column headings, set the index
    mars_table.columns = ["Description","Value"]
    mars_table.set_index ("Description", inplace=True)

    # Write to an HTML Table, and to a string
    mars_table.to_html ("mars_table.html")
    mars_table_html = mars_table.to_html()

    # Add this to the 'mars_info' dictionary
    mars_info.update({'Facts':mars_table_html})


    # Get the pictures of the hemispheres from the USGS AstroGeology website
    # The url for the website
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#    print (f'Getting data from {url}...' )

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Store the results of this cell in a dictionary
    hemisphere_image_urls = []

    # For all all the pictures of the hemispheres of Mars
    for hemisphere in soup.find_all('div', class_='item'):

        # Find the name of the hemisphere
        hemi_name = hemisphere.h3.text.strip()
        
        # Find the detail of the URL of the picture
        detail_url = hemisphere.find('img')['src']

        # Put the base URL in front of the detailed URL
        base_url = "https://astrogeology.usgs.gov"
        img_url = base_url + detail_url
        
        hemisphere_image_urls.append({'title':hemi_name, 'img_url': img_url})
        
    # Add this to the 'mars_info' dictionary
    mars_info.update({'Hemispheres':hemisphere_image_urls})

    # Return the dictionary 'mars_info'
    return (mars_info)
