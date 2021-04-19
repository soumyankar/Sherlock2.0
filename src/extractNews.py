from boilerpy3 import extractors

extractor = extractors.ArticleExtractor()

def extractNews(news_url):
	doc = extractor.get_doc_from_url(news_url)
	articleContent = doc.content
	articleTitle = doc.title
	return articleTitle, articleContent