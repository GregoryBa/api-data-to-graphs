from flask import Flask, render_template, flash, redirect, url_for, request, logging, jsonify
import requests as api_request
import json
import datetime				# Added usage of datetime
from logic import Logic		# All the logic for calculations is placed in this file.

app = Flask(__name__, static_url_path='/static')
headers = {
		"Content-Type": "application/json",
		"Accept": "application/hal+json",
		"x-api-key": "XXX_PUT_A_KEY_HERE"
		}

def get_api_data(headers, url):
	# First call to get first data page from the API
	response = api_request.get(url=url, headers=headers, data=None, verify=False)
	# Convert the response string into json data and get embedded objects
	json_data = json.loads(response.text)
	objects = json_data.get("_embedded").get("objects")
	# Check for more data pages and get thoose too
	nextpage = json_data.get("_links").get("next")
	while nextpage is not None:
		url = nextpage["href"]
		response = api_request.get(url=url, headers=headers, data=None, verify=False)
		json_data = json.loads(response.text)
		objects += json_data.get("_embedded").get("objects")
		nextpage = json_data.get("_links").get("next")
	return objects

# Index page
@app.route('/')
def index():
	return render_template('home.html')

# Overview page for pure text format
@app.route('/overview')
def overview():
	logic = Logic()
	base_url = "XXX_PUT_A_URL_HERE"
	params = "?_limit=50"
	url = base_url + params
	response_deals = get_api_data(headers=headers, url=url)

	average = logic.average_deal_value(response_deals)
	if len(response_deals) > 0:
		wins = logic.number_won(response_deals)
		customers = logic.total_value_won_per_customer(response_deals)
		logic.group_customers(response_deals)
		return render_template('overview.html',
		deals=response_deals,
		average=average,
		wins=wins,
		customers=customers)
	else:
		msg = 'No deals found'
		return render_template('overview.html', msg=msg)

@app.route('/averages')
def averages():
	logic = Logic()
	base_url = "XXX"
	params = "?_limit=50"
	url = base_url + params
	response_deals = get_api_data(headers=headers, url=url)

	if len(response_deals) > 0:
		average = logic.average_deal_value(response_deals)
		return render_template('averages.html', average=average)
	else:
		msg = 'No deals found'
		return render_template('overview.html', msg=msg)

# Function for getting the wins per month for graph
@app.route('/request_wins', methods=['GET', 'POST'])
def request_wins():
	base_url = "XXX"
	params = "?_limit=50"
	url = base_url + params
	response_deals = get_api_data(headers=headers, url=url)

	logic = Logic()
	wins = logic.number_won(response_deals)

	if request.method == 'POST':
		print('Incoming..')
		print(request.get_json())
		return 'OK', 200
	elif request.method == 'GET':
		message = wins
		return jsonify(message)
	else:
		return jsonify('Unknown reqest.')

# Function for getting the value per customer for graph
@app.route('/request_value_per_customer', methods=['GET', 'POST'])
def request_value_per_customer():
	base_url = "XXX"
	params = "?_limit=50"
	url = base_url + params
	response_deals = get_api_data(headers=headers, url=url)

	logic = Logic()
	customers = logic.total_value_won_per_customer(response_deals)

	if request.method == 'POST':
		print('Incoming..')
		print(request.get_json())
		return 'OK', 200
	elif request.method == 'GET':
		message = customers
		return jsonify(message)
	else:
		return jsonify('Unknown reqest.')

@app.route('/customer-status')
def customers():
	logic = Logic()
	base_url = "XXX"
	params = "?_limit=50"
	url = base_url + params
	response_deals = get_api_data(headers=headers, url=url)

	if len(response_deals) > 0:
		customer_stat = logic.group_customers(response_deals)
		return render_template('customer-status.html', customer_stat=customer_stat)
	else:
		msg = 'No deals found'
		return render_template('customer-status.html', msg=msg)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/graphs/wins-last-year')
def graphs_wins_last_year():
    return render_template('wins-last-year.html')

@app.route('/graphs/wins-per-customer')
def graphs_wins_per_customer():
    return render_template('wins-per-customer.html')

if __name__ == '__main__':
	app.secret_key = 'somethingsecret'
	app.run(debug=True)
