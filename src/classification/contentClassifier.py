import argparse
import io
import json
import os

from google.cloud import language_v1
import numpy
import six

def categoryClassify(text, verbose=False):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={'document': document})
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
    if verbose:
        print(text)
        for category in categories:
            print(u"=" * 20)
            print(u"{:<16}: {}".format("category", category.name))
            print(u"{:<16}: {}".format("confidence", category.confidence))

    return result


def sentimentClassify(text, verbose=False):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment    
    # Check if verbose
    if verbose:
    	print("Text: {}".format(text))
    	print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    sentimentScores = {"sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
    return sentimentScores