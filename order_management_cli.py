from order_management import OrderManagement


def main():
    order_management = OrderManagement("user1", "orders.db")

    while True:
        print("What would you like to do?")
        print("1: Add order")
        print("2: Get order")
        print("3: Update order")
        print("4: List all orders")
        print("9: Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            order = input("Enter order: ")
            order_management.add_order(order)
            print("Order added successfully.")
        elif choice == "2":
            order_id = input("Enter order id: ")
            order = order_management.get_order(order_id)
            if order:
                print("Order details:")
                print(f"ID: {order.id}")
                print(f"Order: {order.order}")
                print(f"State: {order.state}")
                print(f"Order Date: {order.order_date}")
                print(f"Estimated Arrival Date: {order.estimated_arrival_date}")
            else:
                print("Order not found.")
        elif choice == "3":
            order_id = input("Enter order id: ")
            new_state = int(input("Enter new state: "))
            if order_management.update_order(order_id, new_state):
                print("Order updated successfully.")
            else:
                print("Failed to update order.")
        elif choice == "4":
            orders = order_management.list_orders()
            if orders:
                print("All orders:")
                for order in orders:
                    print(f"ID: {order.id}")
                    print(f"Order: {order.order}")
                    print(f"State: {order.state}")
                    print(f"Order Date: {order.order_date}")
                    print(f"Estimated Arrival Date: {order.estimated_arrival_date}")
            else:
                print("No orders found.")
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
