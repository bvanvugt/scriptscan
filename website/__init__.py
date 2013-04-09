import urllib2
from urlparse import urlparse

from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, url_for


app = Flask(__name__)

app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))


# Util

def ajax_response(success, data, message):
	return jsonify({
		'success': success,
		'data': data,
		'message': message
	})


def ajax_success(data={}, message=''):
	return ajax_response(True, data, message)


def ajax_failure(data={}, message=''):
	return ajax_response(False, data, message)


def process_script_src(src):
	url_parse = urlparse(src)
	return {
		'raw': src,
		'domain': url_parse.netloc
	}


# Handlers

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/scan')
def scan():
	url = request.args.get('url', None)

	if not url:
		return ajax_failure(message="no URL provided")

	soup = BeautifulSoup(urllib2.urlopen(url).read())
	
	scripts = []
	for script in soup.find_all('script'):
		src = script.get('src')
		if src:
			scripts.append(process_script_src(src))

	return ajax_success(scripts)
