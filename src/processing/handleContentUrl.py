import sys
sys.path.append("..")

from tools.extractNews import ExtractNews
from tools.fetchNews import FetchNews
from classification.contentClassifier import contentClassifier
from classification.extractKeywords import extractKeywords, TextRank4Keyword
from classification.judgmentClassifier import textJudge

import time
import json
# Data to be sent to frontend.
dataURL = {
	"newsURL": "",
	"urlValidity": "true",
	"articleTitle": "",
	"articleTitleJudgment": {},
	"articleContentJudgment": {},
	"articleContent": "",
	"articleCategories": {},
	"sentimentScore": {},
	"articleEntities": {},
	"elapsedTimeScraping": 0,
	"elapsedTimeJudgment": 0,
	"elapsedTimeCategorizing": 0,
	"elapsedTimeFeatures": 0,
	"elapsedTimeNewsAPI": 0,
	"totalExecutionTime": 0
}

def handleContentUrl(newsURL):
	# Scraping Module
	start = time.time() # Verifying elapsed time 	
	articleTitle, articleContent = ExtractNews(newsURL)
	end = time.time()
	elapsedTimeScraping = end - start

	# Judgment Classifier
	start = time.time()
	articleTitleJudgment = textJudge(articleTitle)
	articleContentJudgment = textJudge(articleContent)
	end = time.time()
	elapsedTimeJudgment = end - start

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
	# We will only look for the top 5 keywords.
	extKey = extractKeywords(articleContent)
	articleKeywords = tr4w.get_keywords(5)
	articleEntities = extKey.GetEntities()
	end = time.time()
	elapsedTimeFeatures = end - start

	# Fetching relevant news aritcles frrom NewsAPI

	start = time.time() # Verifying elapsed time 	
	fetchedNewsArticles = FetchNews(articleKeywords)
	end = time.time()
	elapsedTimeNewsAPI = end - start

	# Extract similarity between our content and web crawled news content.
	start = time.time()
	similarityFactors = []
	for article in fetchedNewsArticles:
		similarityFactors.append(extKey.GetSimilarity(article))
	end = time.time()
	elapsedTimeSimilarity = end - start

	# Pass values to frontend.
	dataURL['newsURL'] = newsURL
	dataURL['articleTitle'] = articleTitle
	dataURL['articleTitleJudgment'] = articleTitleJudgment
	dataURL['articleContentJudgment'] = articleContentJudgment
	dataURL['articleContent'] = articleContent
	dataURL['articleCategories'] = articleCategories
	dataURL['sentimentScore'] = sentimentScore
	dataURL['articleEntities'] = articleEntities
	dataURL['elapsedTimeScraping'] = elapsedTimeScraping
	dataURL['elapsedTimeJudgment'] = elapsedTimeJudgment
	dataURL['elapsedTimeFeatures'] = elapsedTimeFeatures
	dataURL['elapsedTimeCategorizing'] = elapsedTimeCategorizing
	dataURL['elapsedTimeNewsAPI'] = elapsedTimeNewsAPI

	return dataURL