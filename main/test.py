import pandas as pd

# Load the Excel file
file_name = 'FinancialLiteracyAppDatabaseCredit.xlsx'
df = pd.read_excel(file_name)
df = df.iloc[1:]
# Initialize variables
questions = []
current_question = None

# Process the data
for index, row in df.iterrows():
    if pd.notna(row['Questions']):
        if current_question:
            questions.append(current_question)
        current_question = {
            'Description': row['DESCRIPTION'],
            'Question': row['Questions'],
            'AnswerChoices': [],
            'AnswerPointValue': [],
            'AnswerExplanation': []
        }
    if pd.notna(row['AnswerChoices']):
        current_question['AnswerChoices'].append(row['AnswerChoices'])
        current_question['AnswerPointValue'].append(row['AnswerPointValue'])
        current_question['AnswerExplanation'].append(row['AnswerExplanation'])

# Append the last question
if current_question:
    questions.append(current_question)

# Convert to DataFrame for display
processed_df = pd.DataFrame(questions)

# Display the processed data
print(processed_df)