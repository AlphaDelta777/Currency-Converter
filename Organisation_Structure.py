class Vehicle:
    def __init__(self, vehicle_id, model, daily_rate):
        self._vehicle_id = vehicle_id
        self._model = model
        self._daily_rate = daily_rate
    
    def get_description(self):
        return f"{self._model} (ID: {self._vehicle_id})"
    
    def calculate_rental_cost(self, days):
        return self._daily_rate * days

class Truck(Vehicle):
    def __init__(self, vehicle_id, model, daily_rate, cargo_capacity):
        super().__init__(vehicle_id, model, daily_rate)
        self._cargo_capacity = cargo_capacity  
    
    def calculate_rental_cost(self, days):
        base_cost = super().calculate_rental_cost(days)
        return base_cost + 50.0

class ElectricCar(Vehicle):
    def __init__(self, vehicle_id, model, daily_rate, battery_capacity):
        super().__init__(vehicle_id, model, daily_rate)
        self._battery_capacity = battery_capacity # in kWh
        self._features = []
        
    def add_premium_feature(self, feature):
        self._features.append(feature)
        
    def calculate_rental_cost(self, days):
        base_cost = self._daily_rate * days * 0.90
        feature_cost = len(self._features) * 5.0 * days
        return base_cost + feature_cost

truck = Truck("T102", "Ford F-150", 120.0, cargo_capacity=1.5)
ev = ElectricCar("E508", "Tesla Model 3", 90.0, battery_capacity=75)

ev.add_premium_feature("FSD Autopilot")
ev.add_premium_feature("Premium Connectivity")

print(f"Vehicle: {truck.get_description()}")
print(f"5-Day Rental Cost: ${truck.calculate_rental_cost(days=5):.2f}") 

print("\n---")

print(f"Vehicle: {ev.get_description()}")
print(f"5-Day Rental Cost: ${ev.calculate_rental_cost(days=5):.2f}")
