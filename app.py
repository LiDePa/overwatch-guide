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

#create db table for each question
class QuestionsBase(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key = True)
	current_hero = db.Column(db.String(30))
	selected_result = db.Column(db.String(30))
	commonness = db.Column(db.Integer, default = 1)
	#date?
#	def __repr__(self):
#        return '<Task %r>' % self.id
class Question1(QuestionsBase):
	__tablename__ = 'Question1'
class Question2(QuestionsBase):
	__tablename__ = 'Question2'
class Question3(QuestionsBase):
	__tablename__ = 'Question3'
class Question4(QuestionsBase):
	__tablename__ = 'Question4'
class Question5(QuestionsBase):
	__tablename__ = 'Question5'
all_db_tables = [Question1, Question2, Question3, Question4, Question5]


#buttons to each hero in all_hero_names are created by script inside index.html
@app.route('/')
def index():
    return render_template('index.html')


#questions pages for each hero in all_hero_names
#is used to fill database
@app.route('/<hero_name>-questions', methods=['POST', 'GET'])
def questions(hero_name):
	if request.method == 'POST':
		#get results n as strings in format "A_B"
		#where A is the question number and B is the place of the selected hero in all_hero_names
		for n in request.form.getlist("result"):
			db_table = all_db_tables[int(n.split("_")[0]) - 1]
			selected_hero = all_hero_names[int(n.split("_")[1])]
			#if the combination of current_hero and selected_result already exists in table, increase its commonness value
			if db.session.query(db.exists().where(and_(db_table.current_hero == hero_name, db_table.selected_result == selected_hero))).scalar() == True:
				existing_data = db_table.query.filter(and_(db_table.current_hero == hero_name, db_table.selected_result == selected_hero)).first()
				existing_data.commonness += 1
			else:
				new_data = db_table(current_hero = hero_name, selected_result = selected_hero)
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