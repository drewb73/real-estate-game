import random
from property import Property, generate_units, generate_address, generate_price_per_unit, generate_management_fee_percent, generate_rent_per_unit, generate_maintenance_per_unit
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class MarketSnapshot:
    # Stores avg metrics for one property type in a given month
    property_type: str
    avg_price_per_unit: float
    avg_rent_per_unit: float
    avg_cap_rate: float

class MarketAnalytics:
    def __init__(self):
        self.history: Dict[int, List[MarketSnapshot]] = {} # {month: [MarketSnapshots]}
    
    def generate_monthly_samples(self, current_month: int) -> List[MarketSnapshot]:
        """Generates market data with natural variation"""
        property_types = ["Duplex", "Triplex", "Fourplex", "Apartment", "Apartment Complex"]
        monthly_data = []
        
        for prop_type in property_types:
            prices = []
            rents = []
            cap_rates = []
            
            # Generate 100 properties with natural market variation
            for _ in range(100):
                # Create some market fluctuations
                if random.random() < 2:
                    price_multiplier = random.uniform(0.7, 1.5)
                    rent_multiplier = random.uniform(0.6, 1.4)
                else:
                    price_multiplier = random.uniform(0.9, 1.1)
                    rent_multiplier = random.uniform(0.9, 1.1)
                
                prop = Property(
                    property_type=prop_type,
                    address="HIDDEN",
                    units=generate_units(prop_type),
                    price_per_unit=int(generate_price_per_unit() * price_multiplier),
                    management_fee_percent=generate_management_fee_percent(),
                    rent_per_unit=int(generate_rent_per_unit() * rent_multiplier),
                    maintenance_per_unit=generate_maintenance_per_unit()
                )
                prices.append(prop.price_per_unit)
                rents.append(prop.rent_per_unit)
                cap_rates.append(prop.cap_rate)
            
            monthly_data.append(MarketSnapshot(
                property_type=prop_type,
                avg_price_per_unit=sum(prices) / len(prices),
                avg_rent_per_unit=sum(rents) / len(rents),
                avg_cap_rate=sum(cap_rates) / len(cap_rates)
            ))
        
        self.history[current_month] = monthly_data
        return monthly_data
        
    def get_latest_market_data(self) -> List[MarketSnapshot]:
        # returns the most recent market data
        if not self.history:
            return []
        latest_month = max(self.history.keys())
        return self.history[latest_month]
    
    # market trends
    def get_market_trend(self, property_type: str) -> float:
        """Returns percentage change in price from previous month"""
        if len(self.history) < 2:
            return 0.0
            
        current = next((x for x in self.history[max(self.history.keys())] 
                    if x.property_type == property_type), None)
        previous = next((x for x in self.history[max(self.history.keys())-1] 
                    if x.property_type == property_type), None)
        
        if not current or not previous:
            return 0.0
            
        return ((current.avg_price_per_unit - previous.avg_price_per_unit) / 
                previous.avg_price_per_unit) * 100
    
