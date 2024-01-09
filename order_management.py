import shelve
import uuid
from datetime import datetime, timedelta
from typing import List, Optional


class OrderWithState:
    """
    Represents an order with its state.

    Attributes:
        id (str): The ID of the order.
        order (str): The order details.
        state (int): The state of the order.
        order_date (datetime): The date the order was placed.
        estimated_arrival_date (datetime): The estimated arrival date of the order.
    """

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
        """
        Converts the OrderWithState object to a dictionary.
        
        Returns:
            dict: The dictionary representation of the OrderWithState object.
        """
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
        """
        Initialize the OrderManagement class.

        Args:
            user_identifier (str): The identifier of the user.
            db_file (str): The file path of the database.

        """
        self.user_identifier = user_identifier
        self.db_file = db_file
    
    def add_order(self, order: str) -> None:
        """
        Add a new order to the user's list of orders.

        Args:
            order (str): The order to be added.

        Raises:
            ValueError: If user_identifier is None.

        """
        print("Entering add_order method")
        if self.user_identifier is None:
            raise ValueError("user_identifier cannot be None")
        with shelve.open(self.db_file) as db:
            print("Opened database")
            if self.user_identifier not in db:
                print("User not found in database. Creating new entry.")
                db[self.user_identifier] = []
            orders: List[OrderWithState] = db[self.user_identifier]
            print("Retrieved user's orders from database")
            order_id = str(uuid.uuid4())
            print("Generated order ID:", order_id)
            order_date = datetime.now()
            print("Current date and time:", order_date)
            estimated_arrival_date: datetime = datetime.now() + timedelta(days=10)
            print("Estimated arrival date:", estimated_arrival_date)
            new_order = OrderWithState(
                order_id, order, 0, order_date, estimated_arrival_date
            )
            print("Created new order:", new_order)
            orders.append(new_order)
            print("Added new order to user's list of orders")
            db[self.user_identifier] = orders
            print("Updated database with modified list of orders")
    
    def get_order(self, order_id: str) -> Optional[OrderWithState]:
        """
        Get the order with the specified order ID.

        Args:
            order_id (str): The ID of the order.

        Returns:
            Optional[OrderWithState]: The order with the specified ID, or None if not found.

        """
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for order in orders:
                    if order.id == order_id:
                        return order
        return None
    
    def get_all_orders(self) -> List[OrderWithState]:
        """
        Get all orders of the user.

        Returns:
            List[OrderWithState]: The list of all orders of the user.

        """
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                return db[self.user_identifier]
        return []
    
    def update_order(self, updated_order: OrderWithState) -> bool:
        """
        Update an existing order.

        Args:
            updated_order (OrderWithState): The updated order.

        Returns:
            bool: True if the order is updated successfully, False otherwise.

        """
        with shelve.open(self.db_file) as db:
            if self.user_identifier in db:
                orders: List[OrderWithState] = db[self.user_identifier]
                for i, order in enumerate(orders):
                    if order.id == updated_order.id:
                        orders[i] = updated_order
                        db[self.user_identifier] = orders
                        return True
        return False
