from boilerpy3 import extractors

extractor = extractors.ArticleExtractor()

def extractNews(news_url):
	doc = extractor.get_doc_from_url(news_url)
	content = doc.content
	title = doc.title
	return NewsTitle, NewsContent