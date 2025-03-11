from flask import Flask, render_template, request
import csv

app = Flask(__name__)


def load_data(file_name):
    data = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # Skip the first row
        headers = next(reader)  # Read the actual headers
        headers = [header.strip() for header in headers if header.strip()]  # Filter out empty headers
        print("Headers:", headers)  # Debugging statement
        for row in reader:
            # Create a dictionary for each row
            row_dict = {headers[i]: row[i].strip() for i in range(len(headers))}
            data.append(row_dict)
    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/survey', methods=['POST'])
def survey():
    choice = request.form.get('survey_choice')
    if choice == 'Loan':
        data = load_data('finalFinancialLiteracyAppDatabaseLoans.CSV')
    else:
        data = load_data('finalFinancialLiteracyAppDatabaseCredit.csv')
    return render_template('survey.html', data=data)


@app.route('/submit', methods=['POST'])
def submit():
    selected_answers = request.form
    results = []
    data = load_data('finalFinancialLiteracyAppDatabaseLoans.CSV') if 'Loan' in selected_answers else load_data(
        'finalFinancialLiteracyAppDatabaseCredit.csv')
    for key, value in selected_answers.items():
        for row in data:
            if row['Questions'] == key and row['AnswerChoices'] == value:
                results.append({
                    'question': key,
                    'answer': value,
                    'point_value': row['AnswerPointValue'],
                    'explanation': row['AnswerExplanation']
                })
    print("Results:", results)  # Debugging statement
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
