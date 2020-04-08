from splinter import Browser
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time

def scrape():
    # Initialize browser with chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    time.sleep(2)

    #NASA Mars News
    # Have browser visit NASA Mars News Site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(0.5)
    # Pull url html and run BeautifulSoup
    html = browser.html
    soup = bs(html,"lxml")
    # Latest headline is stored in an 'a' tag in a div with class 'content_title'
    # Those are stored in the gallery list: 'ul' with class 'item_list'
    news_gallery = soup.find('ul',{'class':'item_list'})
    news_div = news_gallery.find('div',{'class':'content_title'})
    news_title = news_div.find('a').text
    # Paragraph teaser is in div with class 'article_teaser_body'
    news_p = soup.find('div',{'class':'article_teaser_body'}).text


    #JPL Mars Space Images - Featured Image
    # Have browser visit JPL Space Imagery Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(0.5)
    # Reset html and soup
    html = browser.html
    soup = bs(html,'lxml')
    # Find (full-size) featured image url
    # 'ul' with class 'articles' then the first 'a' with class 'fancybox'
    # 'data-fancybox-href' attribute holds the largesize image
    jpl_base_url = "https://www.jpl.nasa.gov"
    jpl_articles = soup.find('ul',{'class':'articles'})
    featured_image_url = jpl_base_url + jpl_articles.find('a',{'class':'fancybox'})['data-fancybox-href']


    #Mars Weather
    # Visit https://twitter.com/marswxreport?lang=en
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    # Sleep to let page load
    time.sleep(3)
    # Scroll the page down to load tweets
    browser.execute_script("window.scrollTo(400, document.body.scrollHeight);")
    # Sleep again to led page load
    time.sleep(3)
    # Reset html and soup
    html = browser.html
    soup = bs(html,'lxml')
    # Reset html and soup
    html = browser.html
    soup = bs(html,'lxml')
    mars_weather = soup.find('span',text=re.compile('^InSight sol')).text


    #Mars Facts
    # Visit https://space-facts.com/mars/
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    # Manually find table is index 0
    # for table in tables:
    #     print(table)
    mars_table = tables[0]
    html_table = mars_table.to_html(header=False,index=False, classes=['table'])


    #Mars Hemispheres
    # Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(0.5)
    # Reset html and soup
    html = browser.html
    soup = bs(html,'lxml')
    # Because of duplicate urls between link image and link text, do 2 .find's
    items = soup.find_all('div',{'class':'item'})
    page_urls = []
    for div in items:
        page_urls.append("https://astrogeology.usgs.gov" + div.find('a',{'class':'itemLink product-item'})['href'])

    hemisphere_image_urls = []
    # Cycle through hemisphere pages and pull the data
    for page in page_urls:
        # Manipulate browser and reset soup
        browser.visit(page)
        html = browser.html
        soup = bs(html,'lxml')

        # Find data
        img_dict = {}
        img_dict['img_url'] = "https://astrogeology.usgs.gov" + soup.find('img',class_='wide-image')['src']
        img_dict['title'] = soup.find('h2',{'class':'title'}).text[:-9]

        #Append img_dict to hemisphere_image_urls
        hemisphere_image_urls.append(img_dict)

    browser.quit()

    # Append all scraped data to return dictionary
    ret_dict = {'news_title':news_title,'news_p':news_p,
               'featured_image_url':featured_image_url,
               'mars_weather':mars_weather,
               'html_table':html_table,
               'hemisphere_image_urls':hemisphere_image_urls
               }
    return ret_dict

#print(scrape())