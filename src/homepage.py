from flask import Flask, request, redirect, url_for, Blueprint, render_template
from tools.extractNews import ExtractNews
from tools.urlHandling import URLValidator
from tools.fetchNews import FetchNews
from classification.contentClassifier import contentClassifier
from classification.extractKeywords import extractKeywords, TextRank4Keyword
from processing.handleContentRaw import handleContentRaw
from processing.handleContentUrl import handleContentUrl

import time
import json
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@homepage.route('/', methods=['POST'])
def render():
	data = json.loads(request.get_data())
	startTime = time.time()
	contentType = data['contentType']
	print ("content Type = " , contentType)
	articleContent = ""
	if contentType == "raw":
		articleContent = data['searchQuery']
		response = handleContentRaw(articleContent)
	if contentType == "url":
		newsURL = data['searchQuery']
		urlValidity = URLValidator(newsURL)
		if(urlValidity == False):
			return render_template('debug.html', urlValidity = urlValidity) # Gotta remap this to 404 on the main content.
		response = handleContentUrl(newsURL)
	endTime = time.time()
	totalExecutionTime = endTime - startTime
	# Total Execution Time.
	response['totalExecutionTime'] = totalExecutionTime

	return json.dumps(response)