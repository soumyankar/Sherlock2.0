from flask import Flask, request, redirect, url_for, Blueprint, render_template
aboutus = Blueprint("about-us", __name__, static_folder="../static", template_folder="../templates")

@aboutus.route('/about-us', methods=['GET'])
def renderPage():
	return render_template('about-us.html')
