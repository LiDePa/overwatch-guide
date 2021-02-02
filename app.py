from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import json, os, sys



app = Flask(__name__)



#get all hero and map names from json files in static folder and fill the according arrays
all_hero_names = []
all_map_names = []
all_map_types = []

######################not sure if os.path works on a web server#####################
path_hero = os.path.join(app.root_path, 'static', 'all_hero_names.json')
with open(path_hero) as (data_hero):
    all_hero_names = json.load(data_hero)

path_map = os.path.join(app.root_path, 'static', 'all_map_names.json')
with open(path_map) as (data_map):
	map_list = json.load(data_map)
	for i in range(len(map_list)):
		all_map_names.append(map_list[i]['map_name'])
		if (map_list[i]['map_type'] != map_list[i-1]['map_type']):
			all_map_types.append(map_list[i]['map_type'])



#initialize database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy(app)

#create db table for each question
class QuestionsBase(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key = True)
	current_hero = db.Column(db.String(30))
	selected_result = db.Column(db.String(30))
	commonness = db.Column(db.Integer, default = 1)
	def __repr__(self):
		return '<result %r>' % self.id
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
class Question6(QuestionsBase):
	__tablename__ = 'Question6'
class Question7(QuestionsBase):
	__tablename__ = 'Question7'
class Question8(QuestionsBase):
	__tablename__ = 'Question8'
class Question9(QuestionsBase):
	__tablename__ = 'Question9'
#array with all tables to iterate through
all_question_tables = [Question1, Question2, Question3, Question4, Question5, Question6, Question7, Question8, Question9]



@app.route('/')
def index():
    return render_template('index.html')



#function to analyse and commit the result of the questions page to the database
def commitResult(current_hero, selected_result, result_table):
	#if the combination of current_hero and selected_result already exists in result_table, increase its commonness value
	existing_data = result_table.query \
		.filter(result_table.current_hero==current_hero) \
		.filter(result_table.selected_result==selected_result) \
		.first()
	if existing_data != None:
		existing_data.commonness += 1
	#otherwise create a new dataset
	else:
		new_data = result_table(current_hero=current_hero, selected_result=selected_result)
		db.session.add(new_data)
	#check if result is valid before comitting
	if selected_result in (all_hero_names + all_map_names + all_map_types) and current_hero in all_hero_names:
		db.session.commit()

#QUESTIONS PAGE for each hero in all_hero_names
#which are used to fill database
@app.route('/<current_hero>-questions', methods=['POST', 'GET'])
def questions(current_hero):
	if request.method == 'POST':
		#get results as strings in format "A_B"
		#where A is the user selected checkbox (selected_result) and B is the table number it belongs to (result_table)
		for result in request.form.getlist('result'):
			commitResult(current_hero, result.split('_')[0], all_question_tables[int(result.split('_')[1]) - 1])
		flash('Thank you for adding your knowledge to Rock-Pharah-Scissors! Feel free to contribute to other heroes as well:')
		return redirect(url_for('index'))
	else:
		#check if url actually contains a hero
		if current_hero in all_hero_names:
			return render_template('questions.html', current_hero=current_hero)
		else:
			flash('Hero not found.')
			return redirect(url_for('index'))



#function to calculate the sum of all datasets and replace the commonness value of each result with a percentage
def commonnessToPercentage(data):
	sum = 0
	for i in data:
		sum += i.commonness
	for i in data:
		i.commonness = round(100 * i.commonness / sum, 1) 	
	return data

#RESULT PAGE for each hero in all_hero_names
#which display contents of database
@app.route('/<current_hero>-results')
def answers(current_hero):
	#check if url actually contains the name of a hero
	if current_hero in all_hero_names:
		#search for datasets of current hero in database and order them by commonness
		common_results = list()
		for table in all_question_tables:
			data = db.session.query(table) \
				.filter_by(current_hero=current_hero) \
				.order_by(table.commonness.desc()) \
				.all()
			common_results += commonnessToPercentage(data)[0:4]
		return render_template('results.html', current_hero=current_hero, common_results=common_results)
	else: 
		flash('Hero not found.')
		return redirect(url_for('index') + '?r')



if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)