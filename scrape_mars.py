#dependencies
from splinter import Browser
from bs4 import BeautifulSoup

import requests
import pymongo
import tweepy
import time
import pandas as pd

#twitter api keys
from config import consumer_key, consumer_secret, access_token, access_token_secret

#path
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Scrape function
def scrape():
	mars_dict= {}
	mars_dict["mars_news"] = marsNewsTitle()
	mars_dict["mars_paragraph"] = marsNewsP()
	mars_dict["mars_image"] = marsImage()
	mars_dict["mars_weather"] = marsWeather()
	mars_dict["mars_facts"] = marsFacts()
	mars_dict["mars_hemisphere"] = marsHem()
	
	return mars_dict

##NEWS
def marsNewsTitle():
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	article = soup.find("div", class_='list_text')
	news_title = article.find("div", class_="content_title").text
	return news_title

def marsNewsP():
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	article = soup.find("div", class_='list_text')
	news_p = article.find("div", class_ ="article_teaser_body").text
	return news_p

##FEATURED IMAGE
def marsImage():
	image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(image_url)

	#navigating to the page with the featured image
	time.sleep(5)
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(5)
	browser.click_link_by_partial_text('more info')
	time.sleep(5)

	#creating BeautifulSoup object; parse with 'html.parser'
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	#getting image URL
	results = soup.find('article')
	extension = results.find('figure', 'lede').a['href']
	link = "https://www.jpl.nasa.gov"
	featured_image_url = link + extension

	return featured_image_url

##WEATHER
def marsWeather():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	target_user = "@MarsWxReport"
	tweet = api.user_timeline(target_user, count =1)[0]
	mars_weather = (tweet['text'])

	return mars_weather

##FACTS
def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)

    return mars_facts

#HEMISPHERES
def marsHem():

	hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemispheres_url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	mars_hemisphere = []
	
	products = soup.find("div", class_ = "result-list")

	hemispheres = products.find_all("div", class_ = "item")

	for hemisphere in hemispheres:
	    title = hemisphere.find("h3").text
	    title = title.replace("Enhanced", "")
	    extension = hemisphere.find("a")["href"]
	    image_link = "https://astrogeology.usgs.gov/" + extension   
	    browser.visit(image_link)
	    html = browser.html
	    soup=BeautifulSoup(html, "html.parser")
	    downloads = soup.find("div", class_="downloads")
	    image_url = downloads.find("a")["href"]
	    mars_hemisphere.append({"title": title, "img_url": image_url})
	
	return mars_hemisphere




