from flask import Flask, request, redirect, url_for, Blueprint, render_template
from tools.extractNews import ExtractNews
from tools.urlHandling import URLValidator
from tools.fetchNews import FetchNews
from classification.contentClassifier import categoryClassify, sentimentClassify
from classification.extractKeywords import ExtractKeywords, ExtractEntities

import time
import json

homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@homepage.route('/', methods=['POST'])
def render():
	newsUrl = request.form['searchQuery']
	urlValidity = URLValidator(newsUrl)
	if(urlValidity == False):
		return render_template('debug.html', urlValidity = urlValidity)

	startTime = time.time()
	# News article scraping

	start = time.time() # Verifying elapsed time 	
	articleTitle, articleContent = ExtractNews(newsUrl)
	end = time.time()
	elapsedTimeScraping = end - start

	# Google API article categorizing

	start = time.time() # Verifying elapsed time 	
	articleCategories = categoryClassify(articleContent)
	sentimentScore = sentimentClassify(articleContent)
	end = time.time()
	elapsedTimeGoogle = end - start

	# Article Feature Extraction 
	start = time.time() # Verifying elapsed time 	
	articleKeywords = ExtractKeywords(articleContent)
	articleEntities = ExtractEntities(articleContent)
	end = time.time()
	elapsedTimeFeatures = end - start

	# Fetching relevant news aritcles frrom NewsAPI

	start = time.time() # Verifying elapsed time 	
	fetchedNewsArticles = FetchNews(articleKeywords)
	end = time.time()
	elapsedTimeNewsAPI = end - start

	# Pass values to frontend.
	endTime = time.time()
	totalExecutionTime = endTime - startTime
	return json.dumps({'articleTitle:':articleTitle})