from Factory_Method import MotorcycleFactory, CarFactory

def test_motorcycle_factory():
    factory = MotorcycleFactory()
    vehicle = factory.get_vehicle_info()
    assert "Motorcycle" in vehicle

def test_car_factory():
    factory = CarFactory()
    vehicle = factory.get_vehicle_info()
    assert "Car" in vehicle
