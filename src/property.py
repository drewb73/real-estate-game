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
        
        # Consistent expense calculation with base + variation
        base_ratio = 0.35  # Base 35% expense ratio
        variation = random.uniform(-0.05, 0.05)  # ±5% variation
        self._expense_ratio = base_ratio + variation  # Final ratio between 30-40%

    def to_dict(self):
        return {
            "property_type": self.property_type,
            "address": self.address,
            "units": self.units,
            "price_per_unit": self.price_per_unit,
            "management_fee_percent": self.management_fee_percent,
            "rent_per_unit": self.rent_per_unit,
            "maintenance_per_unit": self.maintenance_per_unit,
            "expense_ratio": self._expense_ratio  # Save the ratio for persistence
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
        return self.gross_income * self._expense_ratio  # Use stored ratio
    
    @property
    def net_income(self):
        return self.gross_income - self.total_expenses
    
    @property
    def cap_rate(self):
        if self.total_price == 0:
            return 0
        return (self.net_income / self.total_price) * 100
    
    def __str__(self):
        if self.cap_rate >= 7:
            valuation = "\n🔥🔥 Premium Investment!"
        elif self.cap_rate >= 5.5:
            valuation = "\n🔥 Solid Deal"
        elif self.cap_rate <= 3:
            valuation = "\n⚠️⚠️ Money Pit" 
        elif self.cap_rate <= 4:
            valuation = "\n⚠️ Below Average"
        else:
            valuation = "\n➖ Average"
        
        return f"""Type: {self.property_type}
Address: {self.address}
Units: {self.units}
Price per unit: ${self.price_per_unit:,.2f}
Total Price: ${self.total_price:,.2f}
Rent per unit: ${self.rent_per_unit:,.2f}
Gross Income: ${self.gross_income:,.2f}
Management Fee: ${self.management_fee:,.2f}
Expenses: ${self.total_expenses:,.2f}
Net Income: ${self.net_income:,.2f}
CAP Rate: {self.cap_rate:.2f}%{valuation}"""

# [Rest of your existing functions remain unchanged...]
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
    return random.randint(150_000, 250_000)

def generate_management_fee_percent():
    return random.uniform(5.0, 8.0)

def generate_rent_per_unit():
    return random.randint(1200, 2200)

def generate_maintenance_per_unit():
    return random.randint(200, 800)

def generate_property(property_type):
    """Generates properties with natural CAP rate variation"""
    prop = Property(
        property_type=property_type,
        address=generate_address(),
        units=generate_units(property_type),
        price_per_unit=generate_price_per_unit(),
        management_fee_percent=generate_management_fee_percent(),
        rent_per_unit=generate_rent_per_unit(),
        maintenance_per_unit=generate_maintenance_per_unit()
    )
    
    # Ensure some variety in quality
    if random.random() < 0.3:  # 30% chance of underperforming property
        prop.rent_per_unit *= random.uniform(0.7, 0.9)  # Reduce rent
        prop.price_per_unit *= random.uniform(1.1, 1.3)  # Increase price
    
    return prop

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