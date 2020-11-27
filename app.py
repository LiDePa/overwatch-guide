from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

#array with all hero names which is used to generate all hero pages and buttons
all_hero_names = [
    "Ana", 
    "Ashe", 
    "Baptiste", 
    "Bastion", 
    "Brigitte", 
    "D.Va",
    "Doomfist",
    "Echo",
    "Genji",
    "Hanzo",
    "Junkrat",
    "Lucio",
    "McCree",
    "Mei",
    "Mercy",
    "Moira",
    "Orisa",
    "Pharah",
    "Reaper",
    "Reinhardt",
    "Roadhog",
    "Sigma",
    "Soldier: 76",
    "Sombra",
    "Symmetra",
    "Torbjörn",
    "Tracer",
    "Widowmaker",
    "Winston",
    "Wrecking Ball",
    "Zarya",
    "Zenyatta"]
all_map_names = [
    "Busan",
    "Ilios",
    "Lijiang Tower",
    "Nepal",
    "Oasis",
    "Hanamura",
    "Horizon Lunaar Colony",
    "Paris",
    "Temple of Anubis",
    "Volskaya Industries"
    "Dorado",
    "Havana",
    "Junkertown",
    "Rialto",
    "Route 66",
    "Watchpoint: Gibraltar",
    "Blizzard World",
    "Eichenwalde",
    "Hollywood",
    "King's Row",
    "Numbani"
]

app = Flask(__name__)

#index.html links to all heroes in all_hero_names
#user decides if it links to questions or answers
@app.route('/')
def index():
    return render_template('index.html', all_hero_names=all_hero_names)

#questions page to fill database
@app.route('/<hero_name>-questions')
def questions(hero_name):
    #check if url actually contains a hero
    if hero_name in all_hero_names:
        return render_template('questions.html', hero_name=hero_name, all_hero_names=all_hero_names)
    else: 
        return "Hero not found."

#answers page displays contents of database
@app.route('/<hero_name>-answers')
def answers(hero_name):
    #check if url actually contains a hero
    if hero_name in all_hero_names:
        return render_template('answers.html', hero_name=hero_name, all_hero_names=all_hero_names)
    else: 
        return "Hero not found."


if __name__ == '__main__':
    app.run(debug=True)