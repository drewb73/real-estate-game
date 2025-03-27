from player import initialize_player
from property import Property, generate_property, generate_properties_for_month
from market import MarketAnalytics

# Display portfolio
def display_portfolio(player):
    if not player.properties:
        print("\nYou do not own any properties yet.")
        return
    
    print("\n== Your Real Estate Portfolio ==")
    for i, prop in enumerate(player.properties, start=1):
        print(f"{i}. {prop.address}")
    print("0. Go back to main menu")

    while True:
        choice = input("Enter the number of the property to view details (or 0 to go back): ")
        if choice == "0":
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(player.properties):
                view_property_details(player.properties[choice - 1])
            else:
                print("\nInvalid choice. Please enter a number from the list.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")


def view_property_details(property):
    # Display property details
    print("\n=== Property Details ===")
    print(property)
    print("\n1. Go back to the portfolio")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            break
        else:
            print("\nInvalid choice. Please enter 1.")


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
                    player.available_properties.remove(selected_property)
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
                properties = [prop for prop in player.available_properties if prop.property_type == property_type]
                handle_buy_property(player, properties, property_type)
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")


def display_main_menu(player):
    print(f"\nYear: {player.year}, Month: {player.month}")
    print(f" Current Capital: ${player.capital:,.2f}")
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
            display_market_insights(player)
            input("\nPress Enter to return to main menu...")
        elif choice == "4":
            display_portfolio(player)
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
    
    # generate new properties and market data
    player.available_properties = generate_properties_for_month()
    player.market.generate_monthly_samples(player.month)


    # display results
    print(f"\nAdvanced to {player.year}, {player.month}")
    print("New properties and market data are now available!")

def display_market_insights(player):
    print("\n=== Market Insights ===")
    print(f"Current Month: {player.month}, year: {player.year}")
    print("\nAverage Metrics (Based on 100 sampled properties per type):")
    print("{:<20} {:<15} {:<15} {:<10}".format(
        "Property Type", "Avg Price/Unit", "Avg Rent/Unit", "CAP Rate"
    ))
    
    data = player.market.get_latest_market_data()
    if not data:
        print("\nNo market data available yet!")
        return
        
    for snapshot in data:
        print("{:<20} ${:<14,.2f} ${:<14,.2f} {:<8.2f}%".format(
            snapshot.property_type,
            snapshot.avg_price_per_unit,
            snapshot.avg_rent_per_unit,
            snapshot.avg_cap_rate
        ))
    
    # Add historical comparison if available
    if len(player.market.history) > 1:
        print("\nMarket Trends (vs previous month):")
        current_month = max(player.market.history.keys())
        previous_month = current_month - 1

        if previous_month in player.market.history:
            current_data = {s.property_type: s for s in player.market.history[current_month]}
            previous_data = {s.property_type: s for s in player.market.history[previous_month]}
            
            for prop_type in current_data:
                if prop_type in previous_data:
                    price_change = ((current_data[prop_type].avg_price_per_unit - previous_data[prop_type].avg_price_per_unit) / previous_data[prop_type].avg_price_per_unit) * 100
                    rent_change = ((current_data[prop_type].avg_rent_per_unit - previous_data[prop_type].avg_rent_per_unit) / previous_data[prop_type].avg_rent_per_unit) * 100
                
                print(f"{prop_type}: ")
                print(f"  Price: {'↑' if price_change >=0 else '↓'} {abs(price_change):.1f}%")
                print(f"  Rent: {'↑' if rent_change >=0 else '↓'} {abs(rent_change):.1f}%")
    
    input("\nPress Enter to return to main menu...")


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