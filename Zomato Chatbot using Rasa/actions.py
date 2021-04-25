from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd
import regex as re
import json

from flask import Flask
from flask_mail import Mail, Message

email_body = ""

def price(x):
    if x <= 300:
        return 'low'
    elif (x > 300) and (x<=700):
        return 'medium'
    elif x > 700:
        return 'high'

ZomatoData = pd.read_csv('zomato.csv')
ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
ZomatoData['Price'] = ZomatoData['Average Cost for two'].apply(price)
WeOperate = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi', 'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun', 'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore', 'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa', 'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla', 'Secunderabad', 'Panchkula', 'Mohali']

def RestaurantSearch(City,Cuisine,Budget):
	TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: Cuisine.lower() in x.lower())) & (ZomatoData['City'].apply(lambda x: City.lower() in x.lower())) & (ZomatoData['Price'].apply(lambda x: Budget.lower() in x.lower()))]
	return TEMP[['Restaurant Name','Address','Average Cost for two','Aggregate rating']]

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		print(budget)
		print(cuisine)
		print(loc)
		results = RestaurantSearch(City=loc,Cuisine=cuisine,Budget=budget)
		results.sort_values(by='Aggregate rating', ascending=False, inplace=True)
		response=""
		mail_message=""
		restaurant_found_flag = False
		if results.shape[0] == 0:
			response= "We couldn't find restaurants for the given filters. Can you search with different keywords, please?"
			dispatcher.utter_message("-----"+response)
		else:
			for restaurant in results[:10].sort_values(by='Aggregate rating',ascending = False).iterrows():
				#since mail message is top-10 results, choosing 10 rows for iteration
				mail_message += F"Found {restaurant[1]['Restaurant Name']} in {restaurant[1]['Address']} rated {restaurant[1]['Aggregate rating']} with avg cost {restaurant[1]['Average Cost for two']} \n\n"
				mail_message += '\n'
			for restaurant in results[:5].sort_values(by='Aggregate rating',ascending = False).iterrows():
				response=F"Found {restaurant[1]['Restaurant Name']} in {restaurant[1]['Address'].split()[0]} rated {restaurant[1]['Aggregate rating']} with avg cost {restaurant[1]['Average Cost for two']} \n\n"
				restaurant_found_flag = True
				dispatcher.utter_message("-----"+response)
			dispatcher.utter_message("\n \n Would you want the top 10 results to be mailed to you?")
			global email_body
			email_body = mail_message
		return [SlotSet('location',loc),SlotSet('restaurant_found_flag',restaurant_found_flag)]


class ActionCheckCuisine(Action):
	def name(self):
		return "action_check_cuisine"
	
	def run(self, dispatcher, tracker, domain):
		cuisine = tracker.get_slot("cuisine")
		supported_cuisines = ["american", "chinese", "italian", "mexican", "north indian", "south indian"]
		if cuisine:
			if cuisine.lower() in supported_cuisines:
				return [SlotSet("cuisine_flag", True)]
			else:
				return [SlotSet("cuisine", None)]

class ActionCheckLocation(Action):
	def name(self):
		return "action_check_location"
	
	def run(self, dispatcher, tracker, domain):
		WeOp = [x.lower() for x in WeOperate]
		location = tracker.get_slot("location")
		if location:
			if(any(x==location.lower() for x in WeOp)):
				location_flag = True
				print("The Location flag is is "+str(location_flag))
				return [SlotSet("location_flag", location_flag)]
			else:
				return [SlotSet("location", None)]

#Sending Mail
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#email settings
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'abcd@gmail.com',
	MAIL_PASSWORD = '**************'
	)
mail = Mail(app)

@app.route('/send-mail/')
def send_email(emailid):
	
	with app.app_context():
		try:
			msg = Message("Top Restaurants from your search",sender="abcd@gmail.com",recipients=[emailid])
			msg.body = email_body
			mail.send(msg)
			print('Mail sent!')
			return True
		except Exception as e:
			return False
	return

class ActionSendMail(Action):
	def name(self):
		return 'action_send_email'

	def run(self, dispatcher, tracker, domain):
		email = tracker.get_slot('email')
		if self.validate_email(email):
			if(send_email(email)):
				return [SlotSet('flag_email_sent',True)]
			else:
				dispatcher.utter_message("Sorry, this does not seem like a valid email")
				return [SlotSet('email',None),SlotSet('flag_email_sent',False)]
		else:
			dispatcher.utter_message("Sorry, this does not seem like a valid email")
			return [SlotSet('email',None),SlotSet('flag_email_sent',False)]
	
	def validate_email(self, email):
		#to check for a valid email in place using regex
		pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		check = re.search(pattern, email)
		if check:
			return True
		return False
