from flask import Blueprint, render_template

homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/")
def index():
	return render_template('index.html')