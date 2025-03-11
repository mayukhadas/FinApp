import csv
import json
import logging

def convert_csv_to_json(csv_file_path, json_file_path):
    """
    Converts a CSV file containing loan-related questions and answers
    into a JSON format with the desired structure.

    Args:
        csv_file_path (str): Path to the input CSV file.
        json_file_path (str): Path to the output JSON file.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # Adjust logging level as needed

    questions = []
    current_question = None

    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        # Read the first row to check if it contains headers
        first_row = next(csv_reader)
        if first_row[0].startswith("Question") or any(header.lower() in ["questions", "question"] for header in first_row):
            # Assume first row contains headers
            headers = first_row
        else:
            # Assume first row is not a header row
            headers = next(csv_reader)

        csv_reader = csv.DictReader(csv_file, fieldnames=headers, delimiter='|')

        for row_index, row in enumerate(csv_reader):
            print(f"Processing row {row_index+1}: {row}")  # Print each row for inspection

            if 'Questions' not in row:
                logger.warning(f"Row skipped: Missing 'Questions' column: {row}")
                continue

            try:
                question_text = row['Questions'].strip()
                answer_choice = row['AnswerChoices'].strip()
                answer_point_value = row['AnswerPointValue'].strip()
                answer_explanation = row['AnswerExplanation'].strip()

                if current_question is None or current_question['Questions'] != question_text:
                    if current_question is not None:
                        questions.append(current_question)
                    current_question = {
                        'Questions': question_text,
                        'AnswerChoices': answer_choice,
                        'AnswerPointValue': answer_point_value,
                        'AnswerExplanation': answer_explanation
                    }
                else:
                    current_question['AnswerChoices'] += f"^{answer_choice}"
                    current_question['AnswerPointValue'] += f"^{answer_point_value}"
                    current_question['AnswerExplanation'] += f"^{answer_explanation}"

            except KeyError as e:
                logger.error(f"Missing column in CSV: {e}")
                continue

        if current_question is not None:
            questions.append(current_question)

    print(f"Final questions list: {questions}")  # Print the final questions list

    if questions:  # Check if questions list is not empty before writing to JSON
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(questions, json_file, indent=4)
            logger.info(f'CSV data has been converted to JSON and saved to {json_file_path}')
    else:
        logger.warning("No valid questions found. JSON file not created.")

if __name__ == "__main__":
    csv_file_path = 'finalFinancialLiteracyAppDatabaseLoans.csv'
    json_file_path = 'finalFinancialLiteracyAppDatabaseLoans.json'
    convert_csv_to_json(csv_file_path, json_file_path)
    csv_file_path = 'finalFinancialLiteracyAppDatabaseCredit.csv'
    json_file_path = 'finalFinancialLiteracyAppDatabaseCredit.json'
    convert_csv_to_json(csv_file_path, json_file_path)