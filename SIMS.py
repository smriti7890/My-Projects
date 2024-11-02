import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from nltk.sentiment import SentimentIntensityAnalyzer
import barcode
from barcode.writer import ImageWriter
import io
import base64

class InventoryItem:
    def __init__(self, id, name, quantity, expiration_date, barcode):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.barcode = barcode

class SIMS:
    def __init__(self, db_name="sims_inventory.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()
        self.meal_predictor = MealPreferencePredictor()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory 
                            (id INTEGER PRIMARY KEY, 
                            name TEXT NOT NULL, 
                            quantity INTEGER NOT NULL, 
                            expiration_date TEXT NOT NULL,
                            barcode TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS consumption 
                            (id INTEGER PRIMARY KEY,
                            item_id INTEGER,
                            quantity INTEGER,
                            date TEXT,
                            FOREIGN KEY (item_id) REFERENCES inventory (id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS feedback 
                            (id INTEGER PRIMARY KEY,
                            item_id INTEGER,
                            feedback TEXT,
                            date TEXT,
                            FOREIGN KEY (item_id) REFERENCES inventory (id))''')

    def visualize_consumption(self):
        df = self.analyze_consumption_patterns()
        plt.figure(figsize=(10, 6))
        plt.bar(df['name'], df['total_consumed'])
        plt.title('Consumption Patterns')
        plt.xlabel('Food Item')
        plt.ylabel('Total Consumed')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('consumption_patterns.png')
        print("Consumption pattern visualization saved as 'consumption_patterns.png'")

    def main():
        sims = SIMS()

    while True:
        print("\n1. Add item\n2. View inventory\n3. Check expiring items\n4. Record consumption\n5. Analyze consumption\n6. Add feedback\n7. Analyze feedback\n8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            barcode = input("Enter barcode: ")
            item = InventoryItem(None, name, quantity, expiration_date, barcode)
            sims.add_item(item)
        elif choice == '2':
            print(sims.get_items())
        elif choice == '3':
            print(sims.check_expiring_soon())
        elif choice == '4':
            item_id = int(input("Enter item ID: "))
            quantity = int(input("Enter consumed quantity: "))
            sims.record_consumption(item_id, quantity)
        elif choice == '5':
            print(sims.analyze_consumption_patterns())
            sims.visualize_consumption()
        elif choice == '6':
            item_id = int(input("Enter item ID: "))
            feedback = input("Enter feedback: ")
            sims.add_feedback(item_id, feedback)
        elif choice == '7':
            print(sims.analyze_feedback())
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

    def add_item(self, item):
        self.cursor.execute('''INSERT INTO inventory (name, quantity, expiration_date, barcode) 
                               VALUES (?, ?, ?, ?)''', 
                            (item.name, item.quantity, item.expiration_date, item.barcode))
        self.connection.commit()

    def get_items(self):
        self.cursor.execute('SELECT * FROM inventory')
        return self.cursor.fetchall()

    def check_expiring_soon(self, days=7):
        today = datetime.today()
        expiry_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')
        self.cursor.execute('SELECT * FROM inventory WHERE expiration_date <= ?', (expiry_date,))
        return self.cursor.fetchall()

    def update_quantity(self, item_id, new_quantity):
        self.cursor.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (new_quantity, item_id))
        self.connection.commit()

    def record_consumption(self, item_id, quantity):
        today = datetime.today().strftime('%Y-%m-%d')
        self.cursor.execute('''INSERT INTO consumption (item_id, quantity, date) 
                               VALUES (?, ?, ?)''', (item_id, quantity, today))
        self.connection.commit()

    def analyze_consumption_patterns(self):
        query = '''
        SELECT i.name, SUM(c.quantity) as total_consumed
        FROM inventory i
        JOIN consumption c ON i.id = c.item_id
        GROUP BY i.id
        ORDER BY total_consumed DESC
        '''
        df = pd.read_sql_query(query, self.connection)
        return df

    def add_feedback(self, item_id, feedback):
        today = datetime.today().strftime('%Y-%m-%d')
        self.cursor.execute('''INSERT INTO feedback (item_id, feedback, date) 
                               VALUES (?, ?, ?)''', (item_id, feedback, today))
        self.connection.commit()

    def analyze_feedback(self):
        sia = SentimentIntensityAnalyzer()
        self.cursor.execute('SELECT i.name, f.feedback FROM feedback f JOIN inventory i ON f.item_id = i.id')
        feedbacks = self.cursor.fetchall()
        sentiment_scores = [(name, sia.polarity_scores(feedback)['compound']) 
                            for name, feedback in feedbacks]
        df = pd.DataFrame(sentiment_scores, columns=['item_name', 'sentiment_score'])
        return df.groupby('item_name').mean().sort_values('sentiment_score', ascending=False)

    def generate_barcode(self, item_id):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{item_id:012d}', writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer)
        return base64.b64encode(buffer.getvalue()).decode()

    def predict_meal_preference(self, nutrient_data):
        return self.meal_predictor.predict(nutrient_data)

    def __del__(self):
        self.connection.close()

class MealPreferencePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        print(f"Model R-squared score: {score}")

    def predict(self, X):
        return self.model.predict(X)

if __name__ == "__main__":
    sims = SIMS()

    # Add some inventory items. This will obviously be much bigger when this gets officially approved.
    apple = InventoryItem(None, 'Apples', 50, '2024-03-01', '1234567890123')
    banana = InventoryItem(None, 'Bananas', 30, '2023-11-20', '2345678901234')
    sims.add_item(apple)
    sims.add_item(banana)

    print("All items:", sims.get_items())

    print("Expiring soon:", sims.check_expiring_soon())

    sims.update_quantity(1, 45)
    print("Updated inventory:", sims.get_items())

    sims.record_consumption(1, 5)
    sims.record_consumption(2, 3)

    print("Consumption patterns:")
    print(sims.analyze_consumption_patterns())

    sims.add_feedback(1, "The apples were very fresh and tasty!")
    sims.add_feedback(2, "The bananas were a bit overripe.")
    print("Feedback analysis:")
    print(sims.analyze_feedback())

    barcode_image = sims.generate_barcode(1)
    print(f"Barcode generated for item 1")

    # This is a simplified example. When this project is officially approved, I'm going to add in actual nutritional data
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Example nutrient data
    y = np.array([1, 2, 3])  # Example preference scores
    sims.meal_predictor.train_model(X, y)

    new_meal = np.array([[2, 3, 4]])
    prediction = sims.predict_meal_preference(new_meal)
    print(f"Predicted meal preference: {prediction}")
