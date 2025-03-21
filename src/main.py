from player import initialize_player

def main():
    # initialize player
    player = initialize_player()

    # Display player info
    print(f"\nPlayer: {player.name}")
    print(f"Capital: {player.capital}")

    # Save progress (for testing)
    player.save()

if __name__ == "__main__":
    main()