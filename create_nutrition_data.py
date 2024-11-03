import json
import os

os.chdir('NCWIT-Projects')

data = {
    "quizzes": [
        {
            "id": 1,
            "difficulty": "easy",
            "questions": [
                {
                    "id": 1,
                    "text": "Which of these is not a macronutrient?",
                    "options": ["Protein", "Carbohydrates", "Vitamins", "Fats"],
                    "correct_answer": "Vitamins"
                },
                {
                    "id": 2,
                    "text": "What is the main function of vitamin C?",
                    "options": ["Energy production", "Antioxidant", "Blood clotting", "Hormone regulation"],
                    "correct_answer": "Antioxidant"
                }
            ]
        }
    ],
    "nutrition_facts": [
        "Eating a variety of colorful fruits and vegetables ensures a wide range of nutrients.",
        "Whole grains provide more fiber and nutrients than refined grains.",
        "Lean proteins are essential for building and repairing body tissues."
    ]
}

with open('nutrition_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("nutrition_data.json has been created successfully.")
