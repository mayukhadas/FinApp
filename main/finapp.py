from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['POST'])
def survey():
    choice = request.form.get('survey_choice')
    if choice == 'Loan':
        data = load_data('finalFinancialLiteracyAppDatabaseLoans.json')
        title = "Consumer Loans Quiz"
        #max_score = 150
    else:
        data = load_data('finalFinancialLiteracyAppDatabaseCredit.json')
        title = "Credit Score Quiz"
        #max_score = 150
    return render_template('survey.html', data=data, title=title)


@app.route('/submit', methods=['POST'])
def submit():
    selected_answers = request.form
    results = []
    data = load_data('finalFinancialLiteracyAppDatabaseLoans.json') if 'Loan' in selected_answers else load_data('finalFinancialLiteracyAppDatabaseCredit.json')
    for key, value in selected_answers.items():
        for row in data:
            if row['Questions'] == key and value in row['AnswerChoices']:
                index = row['AnswerChoices'].index(value)
                results.append({
                    'question': key,
                    'answer': value,
                    'point_value': row['AnswerPointValue'][index],
                    'explanation': row['AnswerExplanation'][index]
                })
    print("Results:", results)  # Debugging statement
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)