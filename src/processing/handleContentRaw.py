import sys
sys.path.append("..")

from tools.fetchNews import FetchNews
from classification.contentClassifier import contentClassifier
from classification.extractKeywords import extractKeywords, TextRank4Keyword
from classification.judgmentClassifier import textJudge

import time
import json
# Data to be sent to frontend.
dataRAW = {
	"articleContent": "",
	"articleContentJudgment": {},
	"articleCategories": {},
	"sentimentScore": {},
	"articleEntities": {},
	"newsSources": {},
	"similarityFactors": {},
	"elapsedTimeJudgment": 0,
	"elapsedTimeSimilarity": 0,
	"elapsedTimeCategorizing": 0,
	"elapsedTimeFeatures": 0,
	"elapsedTimeNewsAPI": 0,
	"totalExecutionTime": 0
}

def handleContentRaw(articleContent):
	# Article Content Judgment
	start = time.time()
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
	fetchedNewsArticles, newsSources = FetchNews(articleKeywords)
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
	dataRAW['articleContent'] = articleContent
	dataRAW['articleCategories'] = articleCategories
	dataRAW['sentimentScore'] = sentimentScore
	dataRAW['articleEntities'] = articleEntities
	dataRAW['newsSources'] = newsSources
	dataRAW['similarityFactors'] = similarityFactors
	dataRAW['elapsedTimeScraping'] = 0 # No point of having this but anyway.
	dataRAW['elapsedTimeJudgment'] = elapsedTimeJudgment
	dataRAW['elapsedTimeSimilarity'] = elapsedTimeSimilarity
	dataRAW['elapsedTimeFeatures'] = elapsedTimeFeatures
	dataRAW['elapsedTimeCategorizing'] = elapsedTimeCategorizing
	dataRAW['elapsedTimeNewsAPI'] = elapsedTimeNewsAPI

	return dataRAW