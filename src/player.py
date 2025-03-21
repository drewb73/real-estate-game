import json
import os

# File to store player data
PLAYER_DATA_FILE = "player_data.json"

# Player Class
class Player:
    def __init__(self, name, capital=10000000):
        self.name = name
        self.capital = capital
        self.properties = []
    
    def save(self):
        # Save player data to file
        data = {
            "name": self.name,
            "capital": self.capital,
            "properties": self.properties
        }
        with open(PLAYER_DATA_FILE, "w") as f:
            json.dump(data, f)
        print(f"Progress saved for {self.name}")
    
    @staticmethod
    def load():
        # Load player data from a file
        if os.path.exists(PLAYER_DATA_FILE):
            with open(PLAYER_DATA_FILE, "r") as file:
                data = json.load(file)
            return Player(data["name"], data["capital"], data["properties"])
        return None

# Function to createa a new player
def create_player():
    name = input("Enter your name: ")
    return Player(name)

# Function to load or initialize a player
def initialize_player():
    player = Player.load()
    if player:
        print(f"Welcome back {player.name}")
    else:
        print("Welcome to the game")
        player = create_player()
    return player


