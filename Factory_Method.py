from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        return "Car engine started with a key."

class Motorcycle(Vehicle):
    def start_engine(self):
        return "Motorcycle engine started with a button."
    
class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self) -> Vehicle:
        pass
    
    def get_vehicle_info(self):
        vehicle = self.create_vehicle()
        return vehicle.start_engine()
    
class MotorcycleFactory(VehicleFactory):
    def create_vehicle(self) -> Vehicle:
        return Motorcycle()
    
class CarFactory(VehicleFactory):
    def create_vehicle(self):
        return Car()
    
motorcycle_factory = MotorcycleFactory()
print(motorcycle_factory.get_vehicle_info())  # Output: Motorcycle engine started with a button.
car_factory = CarFactory()
print(car_factory.get_vehicle_info())         # Output: Car engine started with a key.

