from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)

#get array with all hero names which is used to generate all hero pages and buttons
with open('static/all_hero_names.json') as (d):
    all_hero_names = json.load(d)


#index.html links to all heroes in all_hero_names
#user decides if it links to questions or answers
@app.route('/')
def index():
    return render_template('index.html')

#questions page to fill database
@app.route('/<hero_name>-questions')
def questions(hero_name):
    #check if url actually contains a hero
    if hero_name in all_hero_names:
        return render_template('questions.html', hero_name=hero_name)
    else: 
        return "Hero not found."

#answers page to display contents of database
@app.route('/<hero_name>-answers')
def answers(hero_name):
    #check if url actually contains a hero
    if hero_name in all_hero_names:
        return render_template('answers.html', hero_name=hero_name)
    else: 
        return "Hero not found."


if __name__ == '__main__':
    app.run(debug=True)