class ParkingLot:
    def __init__(self, compact_spots: int, regular_spots: int, large_spots: int):
        """Initializes the parking lot with the given number of spots."""
        self.compact_spots = compact_spots
        self.regular_spots = regular_spots
        self.large_spots = large_spots

    def addCar(self, carType: int) -> bool:
        """Attempts to park a car of the specified type. Returns True if successful, False if no space."""
        if carType == 1:  # Small
            if self.compact_spots > 0:
                self.compact_spots -= 1
                print(f"Parked a compact car. Remaining compact spots: {self.compact_spots}")
                return True
            else:
                print("No compact spots available.")
                return False
        elif carType == 2:  # Regular
            if self.regular_spots > 0:
                self.regular_spots -= 1
                print(f"Parked a regular car. Remaining regular spots: {self.regular_spots}")
                return True
            else:
                print("No regular spots available.")
                return False
        elif carType == 3:  # Large
            if self.large_spots > 0:
                self.large_spots -= 1
                print(f"Parked a large car. Remaining large spots: {self.large_spots}")
                return True
            else:
                print("No large spots available.")
                return False
        else:
            print("Invalid car type specified.")
            return False

if __name__ == "__main__":
    parking_lot = ParkingLot(compact_spots=3, regular_spots=2, large_spots=1)

    print("\n--- Parking Lot Simulation ---")
    parking_lot.addCar(1) 
    parking_lot.addCar(1)  
    parking_lot.addCar(1) 
    parking_lot.addCar(1)  
    
    parking_lot.addCar(2)  
    parking_lot.addCar(2)  
    parking_lot.addCar(2)  
    
    parking_lot.addCar(3) 
    parking_lot.addCar(3) 