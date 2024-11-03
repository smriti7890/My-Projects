from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

class NourishNow:
    def __init__(self):
        self.load_data()

    def load_data(self):
        # In a real-world scenario, this would load from a database
        with open('nutrition_data.json', 'r') as file:
            self.data = json.load(file)
        self.quizzes = self.data['quizzes']
        self.nutrition_facts = self.data['nutrition_facts']

    def get_quiz(self, difficulty):
        suitable_quizzes = [q for q in self.quizzes if q['difficulty'] == difficulty]
        return random.choice(suitable_quizzes) if suitable_quizzes else None

    def check_answer(self, question_id, user_answer):
        for quiz in self.quizzes:
            for question in quiz['questions']:
                if question['id'] == question_id:
                    return user_answer == question['correct_answer']
        return False

    def get_personalized_suggestion(self, quiz_results):
        score = sum(quiz_results.values())
        total = len(quiz_results)
        percentage = (score / total) * 100

        if percentage >= 80:
            return "Great job! Try exploring advanced topics like nutrient interactions and metabolism."
        elif percentage >= 60:
            return "Good effort! Focus on understanding macronutrients and their roles in the body."
        else:
            return "Keep learning! Start with the basics of a balanced diet and essential nutrients."

    def get_nutrition_fact(self):
        return random.choice(self.nutrition_facts)

nourish_now = NourishNow()

@app.route('/quiz/<difficulty>', methods=['GET'])
def get_quiz(difficulty):
    quiz = nourish_now.get_quiz(difficulty)
    if quiz:
        return jsonify(quiz)
    return jsonify({"error": "No quiz found for the given difficulty"}), 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    result = nourish_now.check_answer(data['question_id'], data['user_answer'])
    return jsonify({"correct": result})

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    quiz_results = request.json
    suggestion = nourish_now.get_personalized_suggestion(quiz_results)
    return jsonify({"suggestion": suggestion})

@app.route('/nutrition_fact', methods=['GET'])
def get_nutrition_fact():
    fact = nourish_now.get_nutrition_fact()
    return jsonify({"fact": fact})

if __name__ == '__main__':
    app.run(debug=True)
