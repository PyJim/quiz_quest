import random
import json
import requests
from flask import Flask, render_template, request, session

app = Flask(__name__)

# dictionary of questions to be used
"""questions = [
    {
        'question': 'Which team did Lionel Messi join in the summer of 2021?',
        'options': ['Barcelona', 'PSG', 'Real Madrid', 'Atletico Madrid'],
        'answer': 'PSG'
    },
    {
        'question': 'Who did Manchester United sign from Borussia Dortmund in the summer of 2021?',
        'options': ['Erling Haaland', 'Jadon Sancho', 'Mario Gotze', 'Marco Reus'],
        'answer': 'Jadon Sancho'
    },
    # Add more questions here
]"""

# url of API containing the questions
API_URL = "https://opentdb.com/api.php?amount=20&category=9&difficulty=easy&type=multiple"

# http request to API
data = requests.get(url=API_URL)

# converting API data to json
database = data.json()["results"]

# filtering API results to suit the context
questions = [{key: item[key] for key in item.keys()
              & {'question', 'correct_answer', 'incorrect_answers'}} for item in database]

# total number of questions from the API. 20 in this case
number_of_questions = len(questions)

# user score
score = 0

# home route
@app.route('/')
def index():
    return render_template('index.html')
    
# route to quiz page
@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer == questions[question_id]['correct_answer']:
            result = 'Correct'
            global score
            score += 1
        else:
            result = 'Incorrect'
        return render_template('results.html', result=result, question_id=int(question_id), number_of_questions=int(number_of_questions))
    else:
        alternatives = questions[question_id]["incorrect_answers"]
        alternatives.append(questions[question_id]["correct_answer"])
        random.shuffle(alternatives)
        options = list(set(alternatives))

        return render_template('quiz.html', question=questions[question_id], question_id=int(question_id), number_of_questions=number_of_questions, options=options)

# route to final results page
@app.route('/quiz/final_results', methods=['GET'])
def final_results():
    return render_template('final_results.html', score=score)
if __name__ == '__main__':
    app.run(debug=True)
