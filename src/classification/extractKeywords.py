import spacy
import pytextrank
from collections import Counter
from string import punctuation

# Define all the features and the labels.
nlp = spacy.load('en_core_web_sm') # The spacy model that we'll be using.
label_tag = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY']
label_description = ['People, including fictional characters',
'Nationalities or religious or political groups',
'Buildings, airports, highways or bridges etc.',
'Companies, agencies, instituions etc.',
'Countries, Cities, Towns',
'Non-GPE locations, mountain ranges, bodies of water',
'Objects, vehicles, foods, etc. (Not Servies',
'Named Hurricanes, Battles, Wars, Sports Events, etc.',
'Titles of books, songs etc.',
'Named documents made into laws',
'Any named language',
'Absolute or relative dates or periods',
'Times smaller than a day',
'Percentages, including \'%\' ',
'Monetary values, including unit',
'Measurements , as of weights or distance']
pos_tag = ['PROPN', 'ADJ', 'NOUN', 'NUM'] # 1


def ExtractKeywords(text):
	features = (GetPhrases(text))
	return features

def ExtractEntities(text):
	return GetEntities(text)

def GetPhrases(text, verbose = False):

	# tr = pytextrank.TextRank()
	nlp.add_pipe("textrank")
	# nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

	# text = 'Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered.'
	doc = nlp(text)
	features = {}
	# examine the top-ranked phrases in the document
	limit = 1 
	for p in doc._.phrases:
		if limit > 60: # NewsAPI only support uptil 60 keywords so we wanna keep below that.
			break
		features[limit] = {}
		features[limit]['rank']=p.rank
		features[limit]['count']=p.count
		features[limit]['text']=p.text
		limit = limit + 1
		if verbose:
			print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
			print(p.chunks)
	return features

def GetEntities(text):
	text = RemoveDuplicateWords(text)
	doc = nlp(text)
	entities = {}
	inc = 1
	index = -99
	for ent in doc.ents:
		if ent.label_ in label_tag:
			entities[inc] = {}
			entities[inc]['text']=ent.text
			index = label_tag.index(ent.label_)
			entities[inc]['label']=ent.label_
			entities[inc]['description']=label_description[index]
			inc = inc + 1
	return entities

def GetFeatures(text):
	result = []
	doc = nlp(text.lower()) # 2
	for token in doc:
	    # 3
	    if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
	        continue
	    # 4
	    if(token.pos_ in pos_tag):
	        result.append(token.text)
	
	mostCommon = Counter(result).most_common(60)
	commonWords = [('' + x[0]) for x in mostCommon]
	commonWords2 = ' '.join(commonWords)
	doc = nlp(commonWords2)
	result = []
	for token in doc:
			    # 3
	    if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
	        continue
	    # 4
	    if(token.pos_ in pos_tag):
	        result.append([token.pos_, token.text])

	return result

# Helper function for removing duplicate words.
def RemoveDuplicateWords(text):
	words = text.split()
	return (" ".join(sorted(set(words), key=words.index)))