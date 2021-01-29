from flask import Flask, render_template, request
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
all_question_tables = [Question1, Question2, Question3, Question4, Question5, Question6, Question7, Question8, Question9]



@app.route('/')
def index():
    return render_template('index.html')



def commitResult(hero_name, result_value, result_table):
	#if the combination of hero_name and result_value already exists in result_table, increase its commonness value
	#######################could be cleaner, too many db queries##########################
	if db.session.query(db.exists().where( and_( result_table.current_hero==hero_name, result_table.selected_result==result_value) )).scalar() == True:
		existing_data = result_table.query.filter( and_( result_table.current_hero==hero_name, result_table.selected_result==result_value )).first()
		existing_data.commonness += 1
	else:
		new_data = result_table(current_hero = hero_name, selected_result = result_value)
		db.session.add(new_data)
	#check if result is valid before comitting
	if result_value in (all_hero_names + all_map_names + all_map_types) and hero_name in all_hero_names:
		db.session.commit()

#questions pages for each hero in all_hero_names
#which are used to fill database
@app.route('/<hero_name>-questions', methods=['POST', 'GET'])
def questions(hero_name):
	if request.method == 'POST':
		#get results as strings in format "A_B"
		#where A is the user selected checkbox (=result_value) and B is the table number it belongs to (=result_table)
		for result in request.form.getlist('result'):
			result_value = result.split('_')[0]
			result_table = all_question_tables[int(result.split('_')[1]) - 1]
			commitResult(hero_name, result_value, result_table)
		return 'Submitted successfully'
	else:
		#check if url actually contains a hero
		if hero_name in all_hero_names:
			return render_template('questions.html', hero_name=hero_name)
		else:
			return 'Hero not found.'



#results pages for each hero in all_hero_names
#which display contents of database
@app.route('/<hero_name>-results')
def answers(hero_name):
	#check if url actually contains the name of a hero
	if hero_name in all_hero_names:
		filtered_results = list()
		for table in all_question_tables:
			result = db.session.query(table).filter_by(current_hero=hero_name)
			result = result.order_by(table.commonness.desc()).limit(5).all()
			filtered_results += result
		return render_template('results.html', hero_name=hero_name, filtered_results=filtered_results)
	else: 
		return 'Hero not found.'



if __name__ == '__main__':
    app.run(debug=True)