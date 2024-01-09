import unittest
import shelve
from datetime import datetime
import uuid

from order_management import OrderManagement, OrderWithState


class TestOrderManagement(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_db.db"
        self.user_identifier = "test_user"
        self.order_management = OrderManagement(self.user_identifier, self.db_path)

    def tearDown(self):
        with shelve.open(self.db_path) as db:
            db.clear()

    def test_add_order(self):
        order = "Test Order"
        self.order_management.add_order(order)
        with shelve.open(self.db_path) as db:
            orders = db[self.user_identifier]
            self.assertEqual(len(orders), 1)
            self.assertEqual(orders[0].order, order)

    def test_get_order_existing(self):
        order_id = str(uuid.uuid4())
        order = "Test Order"
        new_order = OrderWithState(order_id, order, 0, datetime.now(), None)
        with shelve.open(self.db_path) as db:
            db[self.user_identifier] = [new_order]
        retrieved_order = self.order_management.get_order(order_id)
        self.assertEqual(retrieved_order, new_order)

    def test_get_order_nonexistent(self):
        order_id = str(uuid.uuid4())
        retrieved_order = self.order_management.get_order(order_id)
        self.assertIsNone(retrieved_order)

    def test_update_order_existing(self):
        order_id = str(uuid.uuid4())
        order = "Test Order"
        new_order = OrderWithState(order_id, order, 0, datetime.now(), None)
        with shelve.open(self.db_path) as db:
            db[self.user_identifier] = [new_order]
        new_state = 1
        result = self.order_management.update_order(order_id, new_state)
        self.assertTrue(result)
        with shelve.open(self.db_path) as db:
            updated_orders = db[self.user_identifier]
            self.assertEqual(updated_orders[0].state, new_state)

    def test_update_order_nonexistent(self):
        order_id = str(uuid.uuid4())
        new_state = 1
        result = self.order_management.update_order(order_id, new_state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
