from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import json, os, sys



app = Flask(__name__)



#get all hero and map names from json files in static folder and fill the according arrays
###################### not sure if os.path works on a web server ######################
all_hero_names = []
path_hero = os.path.join(app.root_path, 'static', 'all_hero_names.json')
with open(path_hero) as (data_hero):
    all_hero_names = json.load(data_hero)

all_map_names = []
all_map_types = []
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

#create db tables for each question and vote counter
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
class VoteCounter(db.Model):
	current_hero = db.Column(db.String(30), primary_key = True)
	vote_counter = db.Column(db.Integer, default = 1)
	def __repr__(self):
		return str(self.vote_counter)

#array with all tables to iterate through
all_question_tables = [Question1, Question2, Question3, Question4, Question5, Question6, Question7, Question8, Question9]



def countUpVotes(current_hero):
	existing_data = VoteCounter.query \
		.filter(VoteCounter.current_hero==current_hero) \
		.first()
	if existing_data != None:
		existing_data.vote_counter += 1
	else:
		new_data = VoteCounter(current_hero=current_hero)
		db.session.add(new_data)
	db.session.commit()

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

#function to calculate the sum of all datasets and replace the commonness value of each result with a percentage
def commonnessToPercent(data):
	sum = 0
	for i in data:
		sum += i.commonness
	for i in data:
		i.commonness = round(100 * i.commonness / sum, 1) 	
	return data



#startpage
@app.route('/')
def index():
    return render_template('index.html')

#questions page for each hero in all_hero_names
#fills database
@app.route('/<current_hero>-questions', methods=['POST', 'GET'])
def questions(current_hero):
	#if user submits data
	if request.method == 'POST':
		#count up the according vote counter
		countUpVotes(current_hero)
		#get results as an array of strings in format "A_B"
		#where A is the user selected checkbox (selected_result) and B is the question number it belongs to (result_table)
		for result in request.form.getlist('result'):
			commitResult(current_hero, result.split('_')[0], all_question_tables[int(result.split('_')[1]) - 1])
		flash('Thank you for adding your knowledge to Rock-Pharah-Scissors! Feel free to contribute to other heroes as well.')
		return redirect(url_for('index') + '?q')
	#if user requests data
	else:
		#check if url actually contains a hero
		if current_hero in all_hero_names:
			return render_template('questions.html', current_hero=current_hero)
		else:
			flash('Hero not found.')
			return redirect(url_for('index'))

#result page for each hero in all_hero_names
#displays contents of database
@app.route('/<current_hero>-results')
def results(current_hero):
	#check if url actually contains the name of a hero
	if current_hero in all_hero_names:
		#get amount of votes
		vote_count = VoteCounter.query \
			.filter(VoteCounter.current_hero==current_hero) \
			.first()
		#search for datasets of current hero in database and order them by commonness
		common_results = list()
		for table in all_question_tables:
			data = db.session.query(table) \
				.filter_by(current_hero=current_hero) \
				.order_by(table.commonness.desc()) \
				.all()
			common_results += commonnessToPercent(data)[0:4]
		return render_template('results.html', current_hero=current_hero, common_results=common_results, vote_count=vote_count)
	else: 
		flash('Hero not found.')
		#redirect to index with result buttons instead of question buttons
		return redirect(url_for('index') + '?r')



if __name__ == '__main__':
	app.secret_key = 'vrwtchgd'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)