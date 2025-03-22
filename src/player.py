# File to store player data
import json
import os
from property import Property  # Import the Property class

PLAYER_DATA_FILE = "player_data.json"

class Player:
    def __init__(self, name, difficulty, capital, properties=None, year=1, month=1):
        self.name = name
        self.difficulty = difficulty
        self.capital = capital
        self.properties = properties if properties is not None else []
        self.year = year # Current year
        self.month = month # Current month

    def save(self):
        """Save player data to a file."""
        data = {
            "name": self.name,
            "difficulty": self.difficulty,
            "capital": self.capital,
            "properties": [prop.to_dict() for prop in self.properties],  # Convert Property objects to dictionaries
            "year":self.year, # save current year
            "month": self.month # Save the current month
        }
        with open(PLAYER_DATA_FILE, "w") as file:
            json.dump(data, file)
        print(f"Progress saved for {self.name}!")

    @staticmethod
    def load():
        """Load player data from a file."""
        if os.path.exists(PLAYER_DATA_FILE):
            try:
                with open(PLAYER_DATA_FILE, "r") as file:
                    data = json.load(file)

                if not all(key in data for key in ["name", "difficulty", "capital", "properties"]):
                    raise ValueError("Invalid data format in save file.")

                properties = [Property(
                    property_type=prop["property_type"],
                    address=prop["address"],
                    units=prop["units"],
                    price_per_unit=prop["price_per_unit"],
                    management_fee_percent=prop["management_fee_percent"],
                    rent_per_unit=prop["rent_per_unit"],
                    maintenance_per_unit=prop["maintenance_per_unit"]
                ) for prop in data.get("properties", [])]
                return Player(
                    name=data["name"],
                    difficulty=data["difficulty"],
                    capital=data["capital"],
                    properties=properties,
                    year=data["year"],
                    month=data["month"]
                )
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading save file: {e}. Starting a new game. ")
                os.remove(PLAYER_DATA_FILE)
                return None
        return None

# Function to create a new player
def create_player():
    name = input("Enter your name: ")

    # Difficulty levels
    print("\nChoose your difficulty level:")
    print("1. Easy ($5,000,000)")
    print("2. Medium ($2,500,000)")
    print("3. Hard ($1,000,000)")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        difficulty = "Easy"
        capital = 5_000_000
    elif choice == "2":
        difficulty = "Medium"
        capital = 2_500_000
    elif choice == "3":
        difficulty = "Hard"
        capital = 1_000_000
    else:
        print("Invalid choice, setting difficulty to medium.")
        difficulty = "Medium"
        capital = 2_500_000

    return Player(name, difficulty, capital)

# Function to load or initialize a player
def initialize_player():
    if os.path.exists(PLAYER_DATA_FILE):
        with open(PLAYER_DATA_FILE, "r") as file:
            data = json.load(file)
        saved_name = data.get("name", "Unknown")

        print(f"Welcome back, {saved_name}!")
        print("1. continue your saved game?")
        print("2. Delete Save and Restart")
        choice = input("Enter your choice (1 or 2):")

        if choice == "1":
            # load the saved game
            return Player.load()
        elif choice == "2":
            # delete the saved game and restart
            os.remove(PLAYER_DATA_FILE)
            print("Save file deleted. Restarting game...")
        else:
            print("Invalid choice. Restarting game...")
            return Player.load()
    
    # if no save file exists, create a new player
    print("Welcome to the game!")
    return create_player()

