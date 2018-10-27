from flask import Flask, render_template
from flask_ask import Ask, statement, question
from datetime import datetime
import requests
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
    welcome = "Welcome  to the news app."
    return question(welcome)


@ask.intent("newsProvider")
def newsProvider(category):
	category = category.title()
	if category not in url_info.keys():
		return question("Following Category info is not present.\n Please select a different category.")
	
	url = url_info[category]
	reply = ""
	news_list = get_rss_data(url)
	for index,news_info in enumerate(news_list):
		reply += str(index+1) + " " + news_info["title"] + "\n"

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


@app.route("/", methods=["GET", "POST"])
def index():
	print("Home Page")
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)