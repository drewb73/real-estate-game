from player import initialize_player
from property import Property, generate_property, generate_properties_for_month
from market import MarketAnalytics
import random

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
                view_property_details(player, player.properties[choice - 1])
            else:
                print("\nInvalid choice. Please enter a number from the list.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")

def adjust_property_rent(player, property):
    market_rent = calculate_market_rent(player, property)
    max_increase = market_rent * 1.05  # 5% above market
    
    print(f"\n=== Adjust Rent ===")
    print(f"Current Rent: ${property.rent_per_unit:,.2f}")
    print(f"Recommended Market Rent: ${market_rent:,.2f}")
    print(f"Maximum Recommended: ${max_increase:,.2f} (5% above market)")
    
    while True:
        try:
            new_rent = float(input("Enter new rent amount: $"))
            if new_rent < 0:
                print("Rent cannot be negative!")
                continue
                
            # Check if rent is too high
            if new_rent > max_increase:
                penalty_percent = random.uniform(0.03, 0.08)  # 3-8%
                penalty_amount = property.net_income * penalty_percent
                print(f"\nWarning: Rent is {(new_rent/market_rent-1)*100:.1f}% above market!")
                print(f"This will reduce net income by ${penalty_amount:,.2f} this month")
                
                confirm = input("Confirm this change? (y/n): ").lower()
                if confirm != 'y':
                    continue
                    
                # Apply penalty
                player.capital -= penalty_amount
                print(f"\nApplied penalty of ${penalty_amount:,.2f} due to high rent!")
            
            # Update the rent
            old_rent = property.rent_per_unit
            property.rent_per_unit = new_rent
            print(f"\nRent adjusted from ${old_rent:,.2f} to ${new_rent:,.2f}")
            input("\nPress Enter to continue...")
            break
            
        except ValueError:
            print("Invalid input. Please enter a number.")


def view_property_details(player, property):  # Added player parameter
    # Display property details
    print("\n=== Property Details ===")
    print(property)
    
    market_rent = calculate_market_rent(player, property)
    rent_difference = ((property.rent_per_unit - market_rent) / market_rent) * 100
    
    print(f"\nCurrent Rent: ${property.rent_per_unit:,.2f}")
    print(f"Market Rent: ${market_rent:,.2f} ({rent_difference:+.1f}% difference)")
    
    print("\n1. Go back to portfolio")
    print("2. Adjust Rent")
    
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            break
        elif choice == "2":
            adjust_property_rent(player, property)
            break  # Refresh display after adjustment
        else:
            print("\nInvalid choice. Please enter 1 or 2.")


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
            display_sell_properties_menu(player)
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
    monthly_income = 0
    
    # Update property values with realistic appreciation
    for prop in player.properties:
        # Base monthly appreciation (0.3% to 0.8% = ~4-10% annually)
        base_appreciation = random.uniform(1.003, 1.008)
        
        # Seasonal factors (stronger in spring/summer)
        seasonal_factor = 1.0
        if player.month in [3, 4, 5, 6]:  # Spring/summer
            seasonal_factor = random.uniform(1.002, 1.005)  # +0.2% to +0.5%
        elif player.month in [11, 12, 1]:  # Winter
            seasonal_factor = random.uniform(0.998, 1.002)  # -0.2% to +0.2%
        
        # Market momentum based on price-to-rent ratio
        momentum_factor = 1.0
        if len(player.market.history) > 1:
            current_data = player.market.get_latest_market_data()
            for snapshot in current_data:
                if snapshot.property_type == prop.property_type:
                    price_to_rent = snapshot.avg_price_per_unit / snapshot.avg_rent_per_unit
                    if price_to_rent > 180:  # Overpriced market (slower growth)
                        momentum_factor = random.uniform(0.998, 1.003)
                    else:  # Undervalued market (faster growth)
                        momentum_factor = random.uniform(1.003, 1.008)
        
        # Apply all appreciation factors
        total_appreciation = base_appreciation * seasonal_factor * momentum_factor
        prop.price_per_unit *= total_appreciation
        
        # Calculate monthly income (1/12 of annual net income)
        monthly_income += prop.net_income / 12
    
    # Add accumulated income to player's capital
    player.capital += monthly_income
    
    # Advance time
    player.month += 1
    if player.month > 12:
        player.month = 1
        player.year += 1
    
    # Generate new properties for the new month
    player.available_properties = generate_properties_for_month()
    
    # Generate new market data samples
    player.market.generate_monthly_samples(player.month)
    
    # Display results to player
    print(f"\nAdvanced to {player.year}, Month {player.month}")
    if monthly_income > 0:
        print(f"Received ${monthly_income:,.2f} in rental income!")
    print("New properties and market data are now available!")

def calculate_market_rent(player, property):
    """Get average rent for this property type from market data"""
    current_data = player.market.get_latest_market_data()
    for snapshot in current_data:
        if snapshot.property_type == property.property_type:
            return snapshot.avg_rent_per_unit
    return property.rent_per_unit  # Fallback if no market data

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

def display_sell_properties_menu(player):
    if not player.properties:
        print("\nYou don't own any properties to sell!")
        input("\nPress Enter to return to main menu...")
        return
    
    print("\n=== Sell Properties ===")
    for i, prop in enumerate(player.properties, start=1):
        print(f"{i}. {prop.address} (Value: ${prop.total_price:,.2f})")
    print(f"{len(player.properties)+1}. Back to Main Menu")
    
    while True:
        choice = input(f"\nSelect property to sell (1-{len(player.properties)}) or {len(player.properties)+1} to go back: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(player.properties):
                confirm_sell_property(player, player.properties[choice-1])
                break
            elif choice == len(player.properties)+1:
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def confirm_sell_property(player, property):
    while True:
        print(f"\n=== Sell {property.property_type} ===")
        print(property)
        print(f"\nSell Price: ${property.total_price:,.2f}")
        print("1. Confirm Sale")
        print("2. Back to Properties List")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            player.capital += property.total_price
            player.properties.remove(property)
            print(f"\nSold {property.property_type} at {property.address} for ${property.total_price:,.2f}!")
            input("\nPress Enter to continue...")
            break
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


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