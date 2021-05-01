from newsapi import NewsApiClient
from urllib.parse import urlencode, quote_plus
import urllib.parse
import xml.dom.minidom
import requests

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
  	for j in keywords[i]:
  		qParameter = qParameter + ' OR ' + keywords[i]['text']

  parameters = {'q': qParameter,
  'language': 'en',
  'sortBy':'popularity',
  'apiKey': api_key
  }
  url = 'https://newsapi.org/v2/top-headlines?'
  urlTokens = urlencode(parameters, quote_via=urllib.parse.quote)
  url = url + urlTokens
  # print (url)
  response = requests.get(url)
  print (response.json())