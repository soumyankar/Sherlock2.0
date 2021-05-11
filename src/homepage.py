from flask import Flask, request, redirect, url_for, Blueprint, render_template
from tools.extractNews import ExtractNews
from tools.urlHandling import URLValidator
from tools.fetchNews import FetchNews
from classification.contentClassifier import contentClassifier
from classification.extractKeywords import ExtractEntities, TextRank4Keyword

import time
import json
# Data to be sent to frontend.
data = {
	"newsURL": "",
	"urlValidity": "",
	"articleTitle": "",
	"articleContent": "",
	"articleCategories": {},
	"sentimentScore": {},
	"articleEntities": {},
	"elapsedTimeScraping": 0,
	"elapsedTimeCategorizing": 0,
	"elapsedTimeFeatures": 0,
	"elapsedTimeNewsAPI": 0,
	"totalExecutionTime": 0
}
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@homepage.route('/', methods=['POST'])
def render():
	newsURL = request.form['searchQuery']
	urlValidity = URLValidator(newsURL)
	if(urlValidity == False):
		return render_template('debug.html', urlValidity = urlValidity)

	startTime = time.time()
	# News article scraping

	start = time.time() # Verifying elapsed time 	
	articleTitle, articleContent = ExtractNews(newsURL)
	end = time.time()
	elapsedTimeScraping = end - start

	# Google API article categorizing

	start = time.time() # Verifying elapsed time
	classifier = contentClassifier(articleContent, False) 	
	articleCategories = classifier.categoryClassify()
	sentimentScore = classifier.sentimentClassify()
	end = time.time()
	elapsedTimeCategorizing = end - start

	# Article Feature Extraction 
	start = time.time() # Verifying elapsed time 	
	tr4w = TextRank4Keyword()
	tr4w.analyze(articleContent, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
	articleKeywords = tr4w.get_keywords(10)
	print (articleKeywords)
	articleEntities = ExtractEntities(articleContent)
	end = time.time()
	elapsedTimeFeatures = end - start

	# Fetching relevant news aritcles frrom NewsAPI

	start = time.time() # Verifying elapsed time 	
	# fetchedNewsArticles = FetchNews(articleKeywords)
	end = time.time()
	elapsedTimeNewsAPI = end - start

	# Pass values to frontend.
	endTime = time.time()
	totalExecutionTime = endTime - startTime
	data['newsURL'] = newsURL
	data['urlValidity'] = urlValidity
	data['articleTitle'] = articleTitle
	data['articleContent'] = articleContent
	data['articleCategories'] = articleCategories
	data['sentimentScore'] = sentimentScore
	data['articleEntities'] = articleEntities
	data['elapsedTimeScraping'] = elapsedTimeScraping
	data['elapsedTimeFeatures'] = elapsedTimeFeatures
	data['elapsedTimeCategorizing'] = elapsedTimeCategorizing
	data['elapsedTimeNewsAPI'] = elapsedTimeNewsAPI
	data['totalExecutionTime'] = totalExecutionTime

	return json.dumps(data)