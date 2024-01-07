import shelve
import uuid
from datetime import datetime
from typing import List, Optional

class OrderWithState:
    def __init__(self, id: str, order: str, state: int, order_date: datetime, estimated_arrival_date: Optional[datetime]):
        self.id = id
        self.order = order
        self.state = state
        self.order_date = order_date
        self.estimated_arrival_date = estimated_arrival_date
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrderWithState):
            return self.id == other.id and self.order == other.order and self.state == other.state and self.order_date == other.order_date and self.estimated_arrival_date == other.estimated_arrival_date
        return False

class OrderManagement:
    def __init__(self, user_identifier: str, db_file: str):
        self.user_identifier = user_identifier
        self.db_file = db_file
    
    def add_order(self, order: str) -> None:
        with shelve.open(self.db_file) as db:
            if self.user_identifier not in db:
                db[self.user_identifier] = []  # Create an empty list for the user if it doesn't exist
            orders: List[OrderWithState] = db[self.user_identifier]
            order_id = str(uuid.uuid4())  # Generate a unique order ID
            order_date = datetime.now()  # Get the current date and time
            estimated_arrival_date: Optional[datetime] = None  # Set the estimated arrival date to None initially
            new_order = OrderWithState(order_id, order, 0, order_date, estimated_arrival_date)  # Create a new order with initial state 0
            orders.append(new_order)  # Add the new order to the user's list of orders
            db[self.user_identifier] = orders  # Update the database with the modified list of orders
    
    def get_order(self, order_id: str) -> Optional[OrderWithState]:
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for order in orders:
                    if order.id == order_id:
                        return order  # Return the order if found
        return None  # Return None if the order is not found
    
    def update_order(self, order_id: str, new_state: int) -> bool:
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for order in orders:
                    if order.id == order_id:
                        order.state = new_state  # Update the state of the order
                        db[self.user_identifier] = orders  # Update the database with the modified list of orders
                        return True  # Return True to indicate successful update
        return False  # Return False if the order is not found or update fails
