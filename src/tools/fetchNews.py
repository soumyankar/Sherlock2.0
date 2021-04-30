from newsapi import NewsApiClient
import xml.dom.minidom
import requests

def FetchNews():
  api_file = xml.dom.minidom.parse("../../creds/api_key.xml")
  # Get API KEY
  api_key = api_file.getElementsByTagName('api_key')
  # Turn api key from nodelist to str
  api_key = str(api_key[0].firstChild.nodeValue)
  url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey='+api_key
  response = requests.get(url)
  print (response.json())