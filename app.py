from flask import Flask, render_template
from flask_ask import Ask, statement, question
from datetime import datetime
import json
import random
import feedparser

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

f = open("url_info.json","r")
url_info = json.load(f)


@ask.launch
def new_ask():
    print("Launch invoked")
    combined_key = ""
    for key in url_info.keys():
    	combined_key += key + "\n\n "

    welcome = "Welcome to the news on tips.\n\n Say the news category to get the top10 latest news related to it.\n\n Following are the news categories supported.\n\n  " + combined_key
    return question(welcome)


@ask.intent("newsProvider")
def newsProvider(category):
	category = category.title()
	if category not in url_info.keys():
		return question("Following Category info is not present.\n\n Please select a different category.")
	
	url = url_info[category]
	reply = "The top 10 " + category + " news are as follows: \n\n"
	news_list = get_rss_data(url)
	for index,news_info in enumerate(news_list):
		reply += str(index+1) + " " + "\n\n" + news_info["title"] + "\n\n"

	return question(reply)	
		

def get_rss_data(url):
	news_list = []

	data = feedparser.parse(url)
	entries_list = data["entries"]
	for i in range(10):
		news_info = {}
		entry = entries_list[i]
		print("Title : " + entry["title"])

		summary = entry["summary"].split("<div")[0]
		print("Summary : " + summary)
		
		news_info["title"] = entry["title"]
		news_info["summary"] = summary
		news_list.append(news_info)	

	return news_list	


@ask.intent("AMAZON.FallbackIntent")
def fallback():
	reply = "I didn't understand you.\n Say 'Show me technology news' to show tech related latest news. Similarly you can use another category."
	return question(reply)


@ask.intent("AMAZON.CancelIntent")
def cancel():
	reply = "Closing the news."
	return statement(reply)


@ask.intent("AMAZON.StopIntent")
def fallback():
	reply = "Closing the news."
	return statement(reply)


@ask.intent("AMAZON.HelpIntent")
def fallback():
	reply = "I didn't understand you.\n Say 'Show me technology news' to show tech related latest news. Similarly you can use another category."
	return question(reply)


@ask.intent("AMAZON.NavigateHomeIntent")
def fallback():
	reply = "Closing the news."
	return statement(reply)


@app.route("/", methods=["GET", "POST"])
def index():
	print("Home Page")
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)