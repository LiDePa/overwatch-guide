from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import json, os


app = Flask(__name__)


#get all_hero_names array from json file in static folder
path = os.path.join(app.root_path, 'static', 'all_hero_names.json')
with open(path) as (data):
    all_hero_names = json.load(data)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy(app)

class Question1(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	current_hero = db.Column(db.String(30))
	selected_result = db.Column(db.String(30))
	commonness = db.Column(db.Integer, default = 1)
#	def __repr__(self):
#        return '<Task %r>' % self.id

	

#buttons to each hero in all_hero_names are created by script inside index.html
@app.route('/')
def index():
    return render_template('index.html')


#questions pages for each hero in all_hero_names
#is used to fill database
@app.route('/<hero_name>-questions', methods=['POST', 'GET'])
def questions(hero_name):
	if request.method == 'POST':
		#get selected heroes as position in all_hero_names and turn them into string
		for n in request.form.getlist("hero_result"):
			hero_result = all_hero_names[int(n)]
			#if the combination of current_hero and selected_result already exists in table, increase its commonness value
			if db.session.query(db.exists().where(and_(Question1.current_hero == hero_name, Question1.selected_result == hero_result))).scalar() == True:
				existing_data = Question1.query.filter(and_(Question1.current_hero == hero_name, Question1.selected_result == hero_result)).first()
				existing_data.commonness += 1
			else:
				new_data = Question1(current_hero = hero_name, selected_result = hero_result)
				db.session.add(new_data)
			db.session.commit()
		return "Submitted successfully"
	else:
		#check if url actually contains a hero
		if hero_name in all_hero_names:
			return render_template('questions.html', hero_name=hero_name)
		else:
			return "Hero not found."


#answers pages for each hero in all_hero_names
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