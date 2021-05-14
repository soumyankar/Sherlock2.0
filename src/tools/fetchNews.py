from newsapi.newsapi_client import NewsApiClient
from urllib.parse import urlencode, quote_plus
import urllib.parse
import xml.dom.minidom
import requests
import json

def FetchNews(keywords):
  # Find api_file
  # api_file = xml.dom.minidom.parse("../../creds/api_key.xml")
  # Get API KEY
  # api_key = api_file.getElementsByTagName('api_key')
  # Turn api key from nodelist to str
  qParameter = ""
  # api_key = str(api_key[0].firstChild.nodeValue)
  api_key = '7f56d70b628f45f9b2de4355f63e6a24'
  for i in keywords.keys():
  		qParameter = urllib.parse.quote(keywords[i]['keyword'], safe='') + ' AND ' + qParameter

# We limit web crawling to 20 results because feature extraction might cost us a lot of time.
  qParameter = qParameter[ :-5]
  parameters = {'q': qParameter,
  'language': 'en',
  'sortBy':'popularity',
  'apiKey': api_key
  }
  # We must use the /everything endpoint because the q parameter does nnot work with /top-headlines
  url = 'https://newsapi.org/v2/everything?'
  queryParameters = urlencode(parameters, quote_via=urllib.parse.quote)
  response = requests.get(url, params=queryParameters)
  parsed_json = response.json()
  totalResults = parsed_json['totalResults']
  totalArticles = parsed_json['articles']
  newsSources = []
  newsSourcesCount = []
  newsTitles = []
  newsURLs = []
  newsContents = []
  for article in totalArticles:
    articleSourceName = article['source']['name']
    articleTitle = article['title']
    articleURL = article['url']
    articleContent = article['content']
    if articleSourceName in newsSources:
      index = newsSources.index(articleSourceName)
      newsSourcesCount[index] += 1
    if articleSourceName not in newsSources:
      newsSources.append(articleSourceName)
      newsSourcesCount.append(1)

    newsTitles.append(articleTitle)
    newsURLs.append(articleURL)
    newsContents.append(articleContent[0:200]) # Limiting to 200 characters because we dont have the paid version of News API.

  return newsContents, newsSources