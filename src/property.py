import random

class Property:
    def __init__(self, property_type, address, units, price_per_unit, management_fee_percent, rent_per_unit, maintenance_per_unit):
        self.property_type = property_type
        self.address = address
        self.units = units
        self.price_per_unit = price_per_unit
        self.management_fee_percent = management_fee_percent
        self.rent_per_unit = rent_per_unit
        self.maintenance_per_unit = maintenance_per_unit

    # Add this method to convert the Property object to a dictionary
    def to_dict(self):
        return {
            "property_type": self.property_type,
            "address": self.address,
            "units": self.units,
            "price_per_unit": self.price_per_unit,
            "management_fee_percent": self.management_fee_percent,
            "rent_per_unit": self.rent_per_unit,
            "maintenance_per_unit": self.maintenance_per_unit
        }
    
    @property
    def total_price(self):
        return self.units * self.price_per_unit
    
    @property
    def gross_income(self):
        return (self.units * self.rent_per_unit) * 12
    
    @property
    def management_fee(self):
        return self.gross_income * (self.management_fee_percent / 100)
    
    @property
    def total_expenses(self):
        return (self.maintenance_per_unit * 12 * self.units) + self.management_fee
    
    @property
    def net_income(self):
        return self.gross_income - self.total_expenses
    
    @property
    def cap_rate(self):
        if self.total_price == 0:
            return 0
        return (self.net_income / self.total_price) * 100
    
    def __str__(self):
        return(
            f"Type: {self.property_type}\n"
            f"Address: {self.address}\n"
            f"Units: {self.units}\n"
            f"Price per unit: ${self.price_per_unit:,.2f}\n"
            f"Total Price: ${self.total_price:,.2f}\n"
            f"Rent per unit: ${self.rent_per_unit:,.2f}\n"
            f"Gross Income: ${self.gross_income:,.2f}\n"
            f"Management Fee: ${self.management_fee:,.2f}\n"
            f"Expenses: ${self.total_expenses:,.2f}\n"
            f"Net Income: ${self.net_income:,.2f}\n"
            f"CAP Rate: {self.cap_rate:.2f}%"
        )

STREET_NAMES = ["Oak", "Pine", "Elm", "Maple", "Cedar", "Hill", "Lake", "River", "Park", "Main", "Olive", "Cabernet", "Orchid", "Lily", "Applewood"]
STREET_TYPES = ["St", "Ave", "Blvd", "Ln", "Ct", "Rd", "Dr", "Way"]

def generate_address():
    street_number = random.randint(1, 9999)
    street_name = random.choice(STREET_NAMES)
    street_type = random.choice(STREET_TYPES)
    return f"{street_number:04d} {street_name} {street_type}"

def generate_units(property_type):
    if property_type == "Duplex":
        return 2
    elif property_type == "Triplex":
        return 3
    elif property_type == "Fourplex":
        return 4
    elif property_type == "Apartment":
        return random.randint(5, 15)
    elif property_type == "Apartment Complex":
        return random.randint(16, 150)
    else:
        raise ValueError("Invalid property type")

def generate_price_per_unit():
    return random.randint(175_000, 400_000)  # Fixed typo: `radnint` -> `randint`

def generate_management_fee_percent():
    return random.randint(3, 6)

def generate_rent_per_unit():
    return random.randint(800, 2500)

def generate_maintenance_per_unit():
    return random.randint(500, 1500)

def generate_property(property_type):
    address = generate_address()  # Fixed: Added parentheses to call the function
    units = generate_units(property_type)
    price_per_unit = generate_price_per_unit()
    management_fee_percent = generate_management_fee_percent()
    rent_per_unit = generate_rent_per_unit()
    maintenance_per_unit = generate_maintenance_per_unit()

    return Property(
        property_type=property_type,
        address=address,
        units=units,
        price_per_unit=price_per_unit,
        management_fee_percent=management_fee_percent,
        rent_per_unit=rent_per_unit,
        maintenance_per_unit=maintenance_per_unit
    )

def generate_properties_for_type(property_type, count=5):
    return [generate_property(property_type) for _ in range(count)]

def generate_properties_for_month():
    property_types = ["Duplex", "Triplex", "Fourplex", "Apartment", "Apartment Complex"]
    available_properties = []
    for prop_type in property_types:
        available_properties.extend(generate_properties_for_type(prop_type, count=5))
    return available_properties


if __name__ == "__main__":
    property_types = ["Duplex", "Triplex", "Fourplex", "Apartment", "Apartment Complex"]
    for prop_type in property_types:
        print("\n" + "=" * 40)
        print(f"Generated {prop_type}:")
        property = generate_property(prop_type)
        print(property)


