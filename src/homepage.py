from flask import Flask, request, redirect, url_for, Blueprint, render_template
from extractNews import extractNews
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		# Get url from frontend and Extract url metadata here 
		return
	return render_template('index.html')	
	if __name__=="__main__":
		truth.run(debug=True)

