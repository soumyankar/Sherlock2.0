from flask import Flask, request, redirect, url_for, Blueprint, render_template
from tools.extractNews import ExtractNews
from tools.urlHandling import URLValidator
from classification.contentClassifier import categoryClassify, sentimentClassify
from classification.extractKeywords import ExtractKeywords, ExtractEntities
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		newsUrl = request.form['searchQuery']
		urlValidity = URLValidator(newsUrl)
		if(urlValidity == False):
			return render_template('debug.html', urlValidity = urlValidity)
		articleTitle, articleContent = ExtractNews(newsUrl)
		articleCategories = categoryClassify(articleContent)
		sentimentScore = sentimentClassify(articleContent)
		articleKeywords = ExtractKeywords(articleContent)
		articleEntities = ExtractEntities(articleContent)
		return render_template('debug.html',urlValidity = urlValidity, articleTitle = articleTitle, articleContent = articleContent, articleCategories= articleCategories, sentimentScore= sentimentScore, articleKeywords= articleKeywords, articleEntities = articleEntities)
	return render_template('index.html')	
	if __name__=="__main__":
		truth.run(debug=True)

