import argparse
import io
import json
import os

from google.cloud import language_v1
import numpy
import six

class contentClassifier:
    text = ""
    verbose = False
    # Class Constructor
    def __init__(self, text, verbose):
        self.text = text
        self.verbose = False
        # Initialize Client
        self.language_client = language_v1.LanguageServiceClient()
        # Initialize document 
        self.document = language_v1.Document(
                content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

    def categoryClassify(self):
        """Classify the input text into categories. """
        response = (self.language_client).classify_text(request={'document': (self.document)})
        categories = response.categories

        result = {}
        limit = 1
        for category in categories:
            # Turn the categories into a dictionary of the form:
            # {category.name: category.confidence}, so that they can
            # be treated as a sparse vector.
            result[limit] = {}
            result[limit]['category'] = [category.name] 
            result[limit]['confidence']= category.confidence
            limit = limit + 1
        if self.verbose:
            print(self.text)
            for category in categories:
                print(u"=" * 20)
                print(u"{:<16}: {}".format("category", category.name))
                print(u"{:<16}: {}".format("confidence", category.confidence))

        return result

    def sentimentClassify(self):
        # Detects the sentiment of the text
        sentiment = (self.language_client).analyze_sentiment(request={'document': (self.document)}).document_sentiment    
        # Check if verbose
        if self.verbose:
        	print("Text: {}".format(self.text))
        	print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

        sentimentScores = {"sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
        return sentimentScores