from flask import Flask, render_template, url_for

truth = Flask(__name__)

@truth.route('/')
def index():
	return render_template('index.html')

if __name__=="__main__":
	truth.run(debug=True)