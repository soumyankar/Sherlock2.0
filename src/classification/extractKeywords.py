from collections import OrderedDict
import numpy as np
import spacy
import pytextrank
from collections import Counter
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

# Define all the features and the labels.
nlp = spacy.load('en_core_web_sm') # The spacy model that we'll be using.
nlp.add_pipe("textrank")

class extractKeywords:

    def __init__(self, article):
        self.text = article
        self.text = self.RemoveDuplicateWords(self.text)
        self.doc = nlp(self.text)
        # Labels for Entities
        self.label_tag = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY']
        self.label_description = ['People, including fictional characters',
        'Nationalities or religious or political groups',
        'Buildings, airports, highways or bridges etc.',
        'Companies, agencies, instituions etc.',
        'Countries, Cities, Towns',
        'Hills, mountain ranges, bodies of water',
        'Objects, vehicles, foods, etc. (Not Services)',
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

    def GetEntities(self):
        entities = {}
        inc = 1
        index = -99
        for ent in (self.doc).ents:
        	if ent.label_ in self.label_tag:
        		entities[inc] = {}
        		entities[inc]['text']=ent.text
        		index = (self.label_tag).index(ent.label_)
        		entities[inc]['label']=ent.label_
        		entities[inc]['description']=self.label_description[index]
        		inc = inc + 1
        return entities

    def GetSimilarity(self, text):
        textnlp = nlp(text)
        similarityPercentage = (textnlp.similarity(self.doc)) * 100
        return round(similarityPercentage,2)


    # Helper function for removing duplicate words.
    def RemoveDuplicateWords(self, text):
    	words = text.split()
    	return (" ".join(sorted(set(words), key=words.index)))

# Keyword rankings for the text.
class TextRank4Keyword():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    
    def set_stopwords(self, stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """Print top number keywords"""
        keywords = {}
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            # print(key + ' - ' + str(value))
            keywords[i] = {}
            keywords[i]['keyword'] = key
            keywords[i]['confidence'] = str(value)
            if (i+1) > number:
                break
        return keywords
        
    def analyze(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""
        
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Pare text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight