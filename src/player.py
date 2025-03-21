import json
import os

# File to store player data
PLAYER_DATA_FILE = "player_data.json"

class Player:
    def __init__(self, name, difficulty, capital, properties=None):
        self.name = name
        self.difficulty = difficulty
        self.capital = capital
        self.properties = properties if properties is not None else []

    def save(self):
        """Save player data to a file."""
        data = {
            "name": self.name,
            "difficulty": self.difficulty,
            "capital": self.capital,
            "properties": self.properties
        }
        with open(PLAYER_DATA_FILE, "w") as file:
            json.dump(data, file)
        print(f"Progress saved for {self.name}!")

    @staticmethod
    def load():
        """Load player data from a file."""
        if os.path.exists(PLAYER_DATA_FILE):
            with open(PLAYER_DATA_FILE, "r") as file:
                data = json.load(file)
            
            # Handle missing keys (e.g., if the file was created before adding difficulty)
            name = data.get("name", "Unknown")
            difficulty = data.get("difficulty", "Medium")  # Default to Medium if missing
            capital = data.get("capital", 0)  # Default to 0 if missing
            properties = data.get("properties", [])  # Default to empty list if missing

            return Player(
                name=name,
                difficulty=difficulty,
                capital=capital,
                properties=properties
            )
        return None

# Function to createa a new player
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
    player = Player.load()
    if player:
        print(f"Welcome back, {player.name}!")
        print(f"Dificulty: {player.difficulty}")
        print(f"Capital: {player.capital}")
    else:
        print("Welcome to the game!")
        player = create_player()
    return player


