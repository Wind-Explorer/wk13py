from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from accounts_management import Account

from accounts_management import Account, AccountsManagement
from order_management import OrderManagement, OrderWithState

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        date_of_birth = datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d")
        email = request.form["email"]
        password = request.form["password"]
        gender = int(request.form["gender"])
        receive_newsletters = "receive_newsletters" in request.form

        account_manager = AccountsManagement("accounts")
        new_account = Account(
            first_name,
            last_name,
            date_of_birth,
            email,
            password,
            gender,
            receive_newsletters,
        )
        print(
            "account created: "
            + str(account_manager.create_account(account=new_account))
        )

        return redirect(url_for("home"))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        account_manager = AccountsManagement("accounts")

        user_id = account_manager.login(email, password)
        if user_id is not None:
            print("Login successful, user ID: " + user_id)
            return redirect(url_for("loggedin", userid=user_id))
        else:
            print("Login failed")
            return render_template("login.html", error="Invalid email or password")
    else:
        return render_template("login.html")


@app.route("/loggedin/<userid>", methods=["GET"])
def loggedin(userid):
    print(userid)
    return render_template("loggedin.html", user_id=userid)


@app.route("/get_account_info")
def get_account_info():
    account_id = request.args.get("userid")
    account_manager = AccountsManagement("accounts")
    account: Account = account_manager.get_account_by_id(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.__dict__)


@app.route("/delete_account", methods=["DELETE"])
def delete_account():
    account_id = request.args.get("account_id")
    accounts_manager = AccountsManagement("accounts")
    if account_id:
        result = accounts_manager.delete_account(account_id)
        if result:
            return jsonify({"message": "Account deleted successfully"}), 303
        else:
            return jsonify({"message": "Account not found"}), 404
    else:
        return jsonify({"message": "Account ID is required"}), 400


@app.route("/update_account", methods=["PUT"])
def update_account():
    print("updating acc")
    data = request.json
    account_id = data.get("account_id")
    account_data = data.get("account")

    if not account_id or not account_data:
        return jsonify({"error": "Missing account_id or account data"}), 400

    account = Account(
        first_name=account_data.get("first_name"),
        last_name=account_data.get("last_name"),
        date_of_birth=datetime.strptime(account_data.get("date_of_birth"), "%Y-%m-%d"),
        email=account_data.get("email"),
        password=account_data.get("password"),
        gender=int(account_data.get("gender")),
        receive_newsletters=account_data.get("receive_newsletters"),
        id=account_data.get("id"),
    )

    accounts_management = AccountsManagement("accounts")
    result = accounts_management.update_account(account_id, account)

    if result:
        return jsonify({"message": "Account updated successfully"}), 200
    else:
        return jsonify({"error": "Account not found or data invalid"}), 404


@app.route("/order_management")
def order_management():
    return render_template("ordermanagement.html")


@app.route("/add_order", methods=["POST"])
def add_order():
    user_id = request.form.get("user_id")
    new_order = request.form.get("order")
    print("userid: " + user_id)
    order_management = OrderManagement(user_id, "orders")
    order_management.add_order(new_order)
    return jsonify({"message": "Order added successfully"})


@app.route("/get_order", methods=["GET"])
def get_orders():
    user_id = request.args.get("user_id")
    order_id = request.args.get("order_id")
    order_management = OrderManagement(user_id, "orders")
    order = order_management.get_order(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict())


@app.route("/get_all_orders", methods=["GET"])
def get_all_orders():
    user_id = request.args.get("user_id")
    order_management = OrderManagement(user_id, "orders")
    orders = order_management.get_all_orders()
    return jsonify([order.to_dict() for order in orders])


@app.route("/update_order", methods=["PUT"])
def update_order():
    user_id = request.form.get("user_id")
    order_id = request.form.get("order_id")
    state = int(request.form.get("state"))
    order_date = datetime.strptime(request.form.get("order_date"), "%Y-%m-%d")
    estimated_arrival_date_str = request.form.get("estimated_arrival_date")
    estimated_arrival_date = datetime.strptime(estimated_arrival_date_str, "%Y-%m-%d")

    order_management = OrderManagement(user_id, "orders")
    order = order_management.get_order(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    updated_order = OrderWithState(
        order.id, order.order, state, order_date, estimated_arrival_date
    )
    order_management.update_order(updated_order)

    return jsonify({"message": "Order updated successfully"})


@app.route("/remove_order/<user_id>/<order_id>", methods=["DELETE"])
def remove_order(user_id, order_id):
    print("user_id: " + str(user_id))
    print("order_id: " + str(order_id))
    order_management = OrderManagement(user_id, "orders")
    result = order_management.remove_order(order_id)
    if result:
        return jsonify({"message": "Order removed successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
