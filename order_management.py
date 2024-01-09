import shelve
import uuid
from datetime import datetime, timedelta
from typing import List, Optional


class OrderWithState:
    def __init__(
        self,
        id: str,
        order: str,
        state: int,
        order_date: datetime,
        estimated_arrival_date: datetime,
    ):
        self.id = id
        self.order = order
        self.state = state
        self.order_date = order_date
        self.estimated_arrival_date = estimated_arrival_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order": self.order,
            "state": self.state,
            "order_date": self.order_date,
            "estimated_arrival_date": self.estimated_arrival_date,
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrderWithState):
            return (
                self.id == other.id
                and self.order == other.order
                and self.state == other.state
                and self.order_date == other.order_date
                and self.estimated_arrival_date == other.estimated_arrival_date
            )
        return False


class OrderManagement:
    def __init__(self, user_identifier: str, db_file: str):
        self.user_identifier = user_identifier
        self.db_file = db_file

    def add_order(self, order: str) -> None:
        print("Entering add_order method")
        if self.user_identifier is None:
            raise ValueError("user_identifier cannot be None")
        with shelve.open(self.db_file) as db:
            print("Opened database")
            if self.user_identifier not in db:  # line 28
                print("User not found in database. Creating new entry.")
                db[
                    self.user_identifier
                ] = []  # Create an empty list for the user if it doesn't exist
            orders: List[OrderWithState] = db[self.user_identifier]
            print("Retrieved user's orders from database")
            order_id = str(uuid.uuid4())  # Generate a unique order ID
            print("Generated order ID:", order_id)
            order_date = datetime.now()  # Get the current date and time
            print("Current date and time:", order_date)
            estimated_arrival_date: datetime = datetime.now() + timedelta(
                days=10
            )  # Set the estimated arrival date to be 10 days from now
            print("Estimated arrival date:", estimated_arrival_date)
            new_order = OrderWithState(
                order_id, order, 0, order_date, estimated_arrival_date
            )  # Create a new order with initial state 0
            print("Created new order:", new_order)
            orders.append(new_order)  # Add the new order to the user's list of orders
            print("Added new order to user's list of orders")
            db[
                self.user_identifier
            ] = orders  # Update the database with the modified list of orders
            print("Updated database with modified list of orders")

    def get_order(self, order_id: str) -> Optional[OrderWithState]:
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for order in orders:
                    if order.id == order_id:
                        return order  # Return the order if found
        return None  # Return None if the order is not found

    def get_all_orders(self) -> List[OrderWithState]:
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                return db[
                    self.user_identifier
                ]  # Return the list of orders for the user
        return []  # Return an empty list if the user has no orders or is not found

    def update_order(self, updated_order: OrderWithState) -> bool:
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for i, order in enumerate(orders):
                    if order.id == updated_order.id:
                        orders[i] = updated_order  # Update the order in the list
                        db[
                            self.user_identifier
                        ] = orders  # Update the database with the modified list of orders
                        return True  # Return True to indicate successful update
        return False  # Return False if the order is not found or the user is not found
