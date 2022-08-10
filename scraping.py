# import splinter and beautifulsoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # initiate the headless driver for deployment
    executable_path = {'exectuable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image,
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # stop webdriver and return data
    browser.quit()
    return data

# set up splinter

#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):

    # visit the mars news site

    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try/except for error handling

    try:

        slide_elem = news_soup.select_one('div.list_text')

        #slide_elem.find('div', class_='content_title')

        # use the parent element to find the first 'a' tag and save it as 'news title'

        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # use the parent element to find the paragraph text

        news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
        #news_p
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    # visit url

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup

    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None

    # use the base url to create an absolute url
   
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    #img_url

    return img_url

def mars_facts():

    # mars facts
    try:
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        #df.head()

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

    #df.to_html()

    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    #if running as script, print scraped data
    print(scrape_all()) 
