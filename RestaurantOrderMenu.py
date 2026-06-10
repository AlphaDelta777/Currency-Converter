import time


class MenuItem:

    def __init__(self, name: str, price: float, prep_time_mins: int):
        self.name = name
        self.price = price
        self.prep_time_mins = prep_time_mins

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} ({self.prep_time_mins} mins)"


class Order:
    # Class-level counter to give each order a unique ID
    _id_counter = 1

    def __init__(self):
        self.order_id = Order._id_counter
        Order._id_counter += 1
        self.items = []  # List of MenuItem objects
        self.status = "Pending"  # Pending -> Preparing -> Ready -> Delivered

    def add_item(self, item: MenuItem):
        if self.status == "Pending":
            self.items.append(item)
            print(f"Added {item.name} to Order #{self.order_id}.")
        else:
            print(
                f"Cannot add items. Order #{self.order_id} is already being processed."
            )

    def calculate_total(self, tax_rate: float = 0.08) -> float:
        subtotal = sum(item.price for item in self.items)
        tax = subtotal * tax_rate
        return round(subtotal + tax, 2)

    def __str__(self):
        item_list = ", ".join([item.name for item in self.items])
        return f"Order #{self.order_id} [{self.status}]: {item_list or 'Empty'}"


class RestaurantSystem:

    def __init__(self):
        self.menu = {}  # Stores item_name: MenuItem object
        self.orders = {}  # Stores order_id: Order object

    # Menu Management
    def add_to_menu(self, item: MenuItem):
        self.menu[item.name.lower()] = item

    def display_menu(self):
        print("\n--- RESTAURANT MENU ---")
        if not self.menu:
            print("The menu is currently empty.")
        for item in self.menu.values():
            print(f"- {item}")
        print("-----------------------\n")

    # Order Management
    def place_order(self, order: Order):
        if not order.items:
            print("Cannot place an empty order.")
            return
        self.orders[order.order_id] = order
        print(
            f" Order #{order.order_id} successfully placed! Total (inc. tax): ${order.calculate_total():.2f}"
        )

    def advance_order_status(self, order_id: int):
        """Kitchen/Staff function to update order states."""
        if order_id not in self.orders:
            print("Order not found.")
            return

        order = self.orders[order_id]
        status_pipeline = ["Pending", "Preparing", "Ready", "Delivered"]

        try:
            current_index = status_pipeline.index(order.status)
            if current_index < len(status_pipeline) - 1:
                order.status = status_pipeline[current_index + 1]
                print(f"Update: Order #{order_id} is now **{order.status}**.")
                if order.status == "Ready":
                    print(f" Kitchen Notification: Order #{order_id} is ready for pickup!")
            else:
                print(f"Order #{order_id} has already been delivered.")
        except ValueError:
            print("Unknown order status.")


if __name__ == "__main__":

    cafe = RestaurantSystem()

    cafe.add_to_menu(MenuItem("Burger", 10.99, 12))
    cafe.add_to_menu(MenuItem("Fries", 3.99, 5))
    cafe.add_to_menu(MenuItem("Soda", 2.50, 2))

    cafe.display_menu()

    customer_order = Order()
    burger = cafe.menu.get("burger")
    soda = cafe.menu.get("soda")

    if burger and soda:
        customer_order.add_item(burger)
        customer_order.add_item(soda)

    cafe.place_order(customer_order)

    print("\n--- Kitchen Updates ---")
    cafe.advance_order_status(customer_order.order_id)  # Pending -> Preparing
    cafe.advance_order_status(customer_order.order_id)  # Preparing -> Ready
    cafe.advance_order_status(customer_order.order_id)  # Ready -> Delivered