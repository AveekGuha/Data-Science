Problem Statement:

An Indian startup named 'Foodie' wants to build a conversational bot (chatbot) which can help users discover restaurants across several Indian cities.
 

The main purpose of the bot is to help users discover restaurants quickly and efficiently and to provide a good restaurant discovery experience. The project brief is as follows:

 

The bot takes the following inputs from the user:

City: Take the input from the customer as a text field. For example:

Bot: In which city are you looking for restaurants?

User: anywhere in Delhi

 

Important Notes: 

Your bot should be able to work in all the cities which are mentioned in the dataset provided.
If the location doesn't have 5 restaurants, then the bot should not provide any result for that area.
The bot should be able to identify common synonyms of city names, such as Bangalore/Bengaluru, Mumbai/Bombay etc.
 

Your chatbot should provide results for all the relevant locations mentioned in the dataset while for other locations, it should reply back with something like "We do not operate in that area yet".

 

Cuisine Preference: Take the cuisine preference from the customer. The bot should list out the following six cuisine categories (Chinese, Mexican, Italian, American, South Indian & North Indian) and the customer can select any one out of that. Following is an example for the same:

Bot: What kind of cuisine would you prefer?

Chinese
Mexican
Italian
American
South Indian
North Indian
User: I’ll prefer Italian!

 

Average budget for two people: Segment the price range (average budget for two people) into three price categories: lesser than 300, 300 to 700 and more than 700. The bot should ask the user to select one of the three price categories. For example:

Bot: What price range are you looking at?

Lesser than Rs. 300
Rs. 300 to 700
More than 700
User: in range of 300 to 700

 

While showing the results to the user, the bot should display the top 5 restaurants in a sorted order (descending) of the average Zomato user rating (on a scale of 1-5, 5 being the highest). The format should be: {restaurant_name} in {restaurant_address} has been rated {rating}.


Finally, the bot should ask the user whether he/she wants the details of the top 10 restaurants on email. If the user replies 'yes', the bot should ask for user’s email id and then send it over email. Else, just reply with a 'goodbye' message. The mail should have the following details for each restaurant:

Restaurant Name
Restaurant locality address
The average budget for two people
Zomato user rating



How to install Rasa?


Step 1 - Create a new environment from Anaconda Prompt

conda create -n rasa python==3.8.0



Step 2 - Activate the created environment

conda activate rasa



Step 3 - Install rasa

pip install rasa



Step 4 - Install spacy

pip install spacy==2.2.4



Step 5 - Download the pre-trained model

python -m spacy download en_core_web_md



Step 6 - Link the downloaded pre-trained model from admin mode of Anaconda session

python -m spacy link en_core_web_md en




How to run the chatbot?

Step 1 - In a new Anaconda session, activate the already created environment

conda activate rasa



Step 2 - Go to the path where the rasa folder is present


Step 3 - Training of nlu.md file

rasa train nlu



Step 4 - Test the nlu.md file


rasa shell nlu



Step 5 - Train the core

rasa train



Step 6 - Start the action server

rasa run actions



Step 7 - To create new stories, run the following commands in a new Anaconda session

conda activate rasa
rasa interactive




Step 8 - To run the chatbot, run the following commands in a new Anaconda session

conda activate rasa
rasa shell



Steps done:-

1) All possible intents and synonyms are added in nlu.md file.
2) In domain.yml file, the intents and entities have been declared, and the slots as well as most of the actions are defined.
3) In the actions.py file, the major functions - action_search_restaurants, action_check_location and action_send_mail, are defined. Wile the first function, action_search_restaurants, would search the restaurants based on various user inputs, and action_check_location would validate the user input location, the action_send_mail would ensure to send mail to the user, if he opts for that service.
4) The chatbot has been trained again and again, and using the 'rasa interactive' command, the stories.yml and nlu.yml files are populated with multiple stories, to ensure smooth interface experience for the user.


Updated Files:-
1) data/nlu.md
2) data/nlu.yml
3) data/stories.md
4) data/stories.yml
5) domain.yml
6) actions.py









Contributors : Srinidhi Bhat Nire (nsrinidhibhat6996@gmail.com) & Aveek Guha

Date         : 5th April 2021


*** Download and open the .ipynb file in jupyter notebook