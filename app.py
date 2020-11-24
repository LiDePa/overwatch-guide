from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html', all_hero_names=all_hero_names)

@app.route('/<hero_name>-questions')
def questions(hero_name):
    if hero_name in all_hero_names:
        return render_template('questions.html', hero_name=hero_name)
    else: 
        return "Hero not found."


if __name__ == '__main__':
    app.run(debug=True)