from flask import Flask, request, redirect, url_for, Blueprint, render_template
from extractNews import extractNews
from tools.urlHandling import URLValidator
from classification.contentClassifier import textClassify, sentimentClassify
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		newsUrl = request.form['searchQuery']
		urlValidity = URLValidator(newsUrl)
		if(urlValidity == False):
			return render_template('debug.html', urlValidity = urlValidity)
		articleTitle, articleContent = extractNews(newsUrl)
		articleCategories = textClassify(articleContent)
		sentimentScore = sentimentClassify(articleContent)
		return render_template('debug.html',urlValidity = urlValidity, articleTitle = articleTitle, articleContent = articleContent, articleCategories= articleCategories, sentimentScore= sentimentScore)
	return render_template('index.html')	
	if __name__=="__main__":
		truth.run(debug=True)

