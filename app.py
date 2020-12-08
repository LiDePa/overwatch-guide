from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json, os


app = Flask(__name__)

#get all_hero_names array from json file in static folder
#is used to verify urls
path = os.path.join(app.root_path, 'static', 'all_hero_names.json')
with open(path) as (data):
    all_hero_names = json.load(data)


#buttons to each hero in all_hero_names are created by script inside index.html
@app.route('/')
def index():
    return render_template('index.html')

#questions page for each hero in all_hero_names
#is used to fill database
@app.route('/<hero_name>-questions')
def questions(hero_name):
	#check if url actually contains a hero
	if hero_name in all_hero_names:
		return render_template('questions.html', hero_name=hero_name)
	else:
		return "Hero not found."

#answers page for each hero in all_hero_names
#displays contents of database
@app.route('/<hero_name>-answers')
def answers(hero_name):
	#check if url actually contains a hero
	if hero_name in all_hero_names:
		return render_template('answers.html', hero_name=hero_name)
	else: 
		return "Hero not found."


if __name__ == '__main__':
    app.run(debug=True)