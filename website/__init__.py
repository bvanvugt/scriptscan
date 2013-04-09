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


# Handlers

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/scan')
def scan():
	url = request.args.get('url', None)

	if not url:
		return ajax_failure(message="no URL provided")

	return ajax_success({'brad': url})
