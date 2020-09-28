from datetime import datetime

# Class for all the logic of the website.

class Logic:
    def __init__(self):
        pass

    # Finds if the deal is last year.
    def last_year_deal(self, deal):
    	last_year = int(deal['closeddate'][0:4])
    	if(last_year == (datetime.now().year - 1)): return True
    	else: return False

    # Calculates average deal last year.
    def average_deal_value(self, response_deals):
    	length = 0
    	average = 0
    	for deal in response_deals:
    		if(self.last_year_deal(deal) == True):
    			average += deal['value'] 	# The values from dealstatus are in float
    			length = length + 1
    	average = average / length
    	return average

    def number_won(self, response_deals):
    	wins = [0] * 12
    	for deal in response_deals:
    		key = deal['dealstatus']['key']
    		date_and_time = deal['closeddate']
    		current_month = int(date_and_time[5:7])
    		if key == 'agreement' and self.last_year_deal(deal) == True:
    			wins[current_month - 1] += 1
    	return wins

    def total_value_won_per_customer(self, response_deals):
    	customers_dict = {}
    	cust = ""
    	for deal in response_deals:
    		key = deal['dealstatus']['key']
    		cust = deal['name']
    		val = deal['value']
    		if key == 'agreement' and self.last_year_deal(deal) == True:
    			customers_dict[cust] = val
    	return customers_dict

    def group_customers(self, response_deals):
    	dict_grouping = {}
    	dt = datetime.now()
    	dt_last_year = dt.replace(year=dt.year - 1)
    	dt_last_year = int(dt_last_year.strftime("%Y%m%d"))
    	# Datetime last year: 20190424 type: str

    	# format of time in json:
    	# 2019-06-05 type str
    	for deal in response_deals:
    		dd = deal['closeddate']
    		dd = dd[0:10]
    		deal_date = int(dd.replace('-', ''))
    		cust = deal['name']
    		date = deal['closeddate']
    		if deal['value'] > 0 and deal['dealstatus']['key'] == 'agreement':
    		    if (dt_last_year - deal_date) >= 0:
    			     dict_grouping[cust] = 'customer'
    		    elif not self.last_year_deal(deal):
    			     dict_grouping[cust] = 'inactive'
    		elif deal['value'] == 0.0 and deal['dealstatus'] != 'irrelevant':
    			dict_grouping[cust] = 'prospect'
    	return dict_grouping
