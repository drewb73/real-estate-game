from player import initialize_player
from property import Property, generate_property

# Generate a list of available properties for a sepcific property type
def generate_properties_for_type(property_type, count=5):
    return [generate_property(property_type) for _ in range(count)]

# Display addresses for a sepcific a specific type
def display_properties(properties, property_type):
    print(f"\n== Available {property_type}s ===")
    for i, prop in enumerate(properties, start=1):
        print(f"\nProperty: {i}:")
        print(prop)
    print("\n6. Previous Menu")


# Handle buying a property
def handle_buy_property(player, properties, property_type):
    while True:
        display_properties(properties, property_type)
        choice = input("Enter the number of the property you want to buy (or 6 to go back): ")

        if choice == "6":
            break
        try:
            choice = int(choice)
            if 1 <= choice <= 5:
                selected_property = properties[choice - 1]
                if player.capital >= selected_property.total_price:
                    player.capital -= selected_property.total_price
                    player.properties.append(selected_property)
                    print(f"\nYou bought {selected_property.property_type} at {selected_property.address} for ${selected_property.total_price:,.2f}!")
                    break
                else:
                    print("\nYou don't have enough capital to buy this property.")
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")


def display_buy_properties_menu(player):
    property_types = ["Duplex", "Triplex", "Fourplex", "Apartment", "Apartment Complex"]
    while True:
        print("\n=== Buy Properties ===")
        for i, prop_type in enumerate(property_types, start=1):
            print(f"{i}. Available {prop_type}s")
        print("6. Main Menu")

        choice = input("Enter your choice (1-6): ")
        if choice == "6":
            print("\nReturning to the main menu...")
            return  # Return to the main menu
        try:
            choice = int(choice)
            if 1 <= choice <= 5:
                property_type = property_types[choice - 1]
                properties = generate_properties_for_type(property_type)
                handle_buy_property(player, properties, property_type)
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")


def display_main_menu(player):
    print(f"\nYear: {player.year}, Month: {player.month}")
    print("\n=== Main Menu ===")
    print("1. Buy Available Properties")
    print("2. Sell Owned Properties")
    print("3. View Market Insights")
    print("4. View Real Estate Portfolio")
    print("5. Advance to Next Month")
    print("6. Save and Exit")

def handle_main_menu(player):
    while True:
        display_main_menu(player)
        choice = input("Enter your choice 1-6: ")
        if choice == "1":
            display_buy_properties_menu(player)
        elif choice == "2":
            print("\nSell Owned Properties (WIP)")
        elif choice == "3":
            print("\nView Market Insights (WIP)")
        elif choice == "4":
            print("\nView Real Estate Portfolio (WIP)")
        elif choice == "5":
            advance_to_next_month(player)
        elif choice == "6":
            print("\nExiting the game...")  
            player.save()
            break
        else:
            print("\nInvalid choice. Please try again.")

def advance_to_next_month(player):
    player.month += 1
    if player.month > 12:
        player.month = 1
        player.year += 1
    print(f"\nAdvanced to {player.year}, {player.month}")


def main():
    # initialize player
    player = initialize_player()

    # Display player info
    print(f"\nPlayer: {player.name}")
    print(f"Difficulty: {player.difficulty}")
    print(f"Capital: ${player.capital}")

    # Start the main menu loop
    handle_main_menu(player)

if __name__ == "__main__":
    main()