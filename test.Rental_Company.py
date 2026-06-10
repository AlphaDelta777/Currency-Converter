from Rental_Company import Vehicle, Truck, ElectricCar

def test_vehicle_description():
    vehicle = Vehicle("V100", "Toyota Corolla", 50.0)
    assert vehicle.get_description() == "Toyota Corolla (ID: V100)"

def test_vehicle_rental_cost():
    vehicle = Vehicle("V100", "Toyota Corolla", 50.0)
    assert vehicle.calculate_rental_cost(3) == 150.0
    assert vehicle.calculate_rental_cost(0) == 0.0

def test_truck_rental_cost():
    truck = Truck("T100", "Ford F-150", 100.0, 2.0)
    assert truck.calculate_rental_cost(3) == 350.0

def test_electric_car_cost_no_features():
    ev = ElectricCar("E100", "Tesla Model 3", 100.0, 75)
    assert ev.calculate_rental_cost(2) == 180.0

def test_electric_car_cost_with_features():
    ev = ElectricCar("E100", "Tesla Model 3", 100.0, 75)
    ev.add_premium_feature("Autopilot")
    ev.add_premium_feature("Heated Seats")
    assert ev.calculate_rental_cost(2) == 200.0
