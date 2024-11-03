import json
from datetime import datetime, timedelta
import random

class GrocerifyApp:
    def __init__(self):
        self.inventory = {}
        self.load_recipes()

    def load_recipes(self):
        self.recipes = [
            {
                'title': 'Fruit Salad',
                'ingredients': ['Apples', 'Bananas', 'Oranges'],
                'instructions': 'Chop fruits and mix together.'
            },
            {
                'title': 'Vegetable Stir Fry',
                'ingredients': ['Carrots', 'Broccoli', 'Bell Peppers'],
                'instructions': 'Chop vegetables and stir fry with oil and seasonings.'
            },
            # Add more recipes here
        ]

    def sync_with_smart_fridge(self):
        # Simulate getting data from a smart fridge
        fridge_data = {
            'Apples': '2023-12-15',
            'Milk': '2023-12-10',
            'Carrots': '2023-12-20',
            'Broccoli': '2023-12-18',
            'Chicken': '2023-12-12'
        }
        self.inventory.update(fridge_data)
        print("Synced with smart fridge. Updated inventory.")

    def check_expiring_soon(self, days=3):
        today = datetime.today()
        expiring_soon = []
        for item, exp_date_str in self.inventory.items():
            exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
            if 0 < (exp_date - today).days <= days:
                expiring_soon.append(item)
        return expiring_soon

    def suggest_recipes(self):
        available_ingredients = set(self.inventory.keys())
        suggested_recipes = []
        for recipe in self.recipes:
            if set(recipe['ingredients']).issubset(available_ingredients):
                suggested_recipes.append(recipe)
        return suggested_recipes

    def reduce_waste_tip(self):
        tips = [
            "Freeze overripe fruits for smoothies.",
            "Use vegetable scraps to make homemade stock.",
            "Plan your meals for the week to avoid overbuying.",
            "Store fruits and vegetables properly to extend their life."
        ]
        return random.choice(tips)

    def __str__(self):
        return f'Current Inventory: {json.dumps(self.inventory, indent=2)}'

# Example usage
if __name__ == '__main__':
    app = GrocerifyApp()
    
    app.sync_with_smart_fridge()
    print(app)
    
    print("\nItems expiring soon:", app.check_expiring_soon())
    
    print("\nSuggested Recipes:")
    for recipe in app.suggest_recipes():
        print(f"- {recipe['title']}")
        print(f"  Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"  Instructions: {recipe['instructions']}")
        print()
    
    print("Tip to reduce food waste:", app.reduce_waste_tip())
