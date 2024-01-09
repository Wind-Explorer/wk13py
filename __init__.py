from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from accounts_management import Account

from accounts_management import Account, AccountsManagement
from order_management import OrderManagement, OrderWithState
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 获取表单数据
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
        email = request.form['email']
        password = request.form['password']
        gender = int(request.form['gender'])
        receive_newsletters = 'receive_newsletters' in request.form
        
        account_manager = AccountsManagement("accounts")
        new_account = Account(first_name, last_name, date_of_birth, email, password, gender, receive_newsletters)
        print("account created: " + str(account_manager.create_account(account=new_account)))
        
        # 重定向到首页
        return redirect(url_for('home'))
    else:
        # 显示注册表单
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        email = request.form['email']
        password = request.form['password']
        
        # 创建 AccountsManagement 实例
        account_manager = AccountsManagement("accounts")
        
        # 验证用户的身份
        user_id = account_manager.login(email, password)
        if user_id is not None:
            # 如果用户 ID 不为 None，说明登录成功
            print("Login successful, user ID: " + user_id)
            # 重定向到首页
            return redirect(url_for('loggedin', userid=user_id))
        else:
            # 如果用户 ID 为 None，说明登录失败
            print("Login failed")
            # 重新显示登录表单
            return render_template('login.html', error="Invalid email or password")
    else:
        # 显示登录表单
        return render_template('login.html')
    
@app.route('/loggedin/<userid>', methods=['GET'])
def loggedin(userid):
    print(userid)
    return render_template('loggedin.html', user_id=userid)

@app.route('/get_account_info')
def get_account_info():
    account_id = request.args.get('userid')
    account_manager = AccountsManagement("accounts")
    account: Account = account_manager.get_account_by_id(account_id)
    if account is None:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(account.__dict__)

@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    account_id = request.args.get('account_id')
    accounts_manager = AccountsManagement("accounts")
    if account_id:
        result = accounts_manager.delete_account(account_id)
        if result:
            return jsonify({'message': 'Account deleted successfully'}), 303
        else:
            return jsonify({'message': 'Account not found'}), 404
    else:
        return jsonify({'message': 'Account ID is required'}), 400

@app.route('/order_management')
def order_management():
    return render_template('ordermanagement.html')

@app.route('/add_order', methods=['POST'])
def add_order():
    user_id = request.form.get('user_id')
    new_order = request.form.get('order')
    print("userid: " + user_id)
    order_management = OrderManagement(user_id, "orders")
    order_management.add_order(new_order)
    return jsonify({'message': 'Order added successfully'})

@app.route('/get_order', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    order_id = request.args.get('order_id')
    order_management = OrderManagement(user_id, "orders")
    order = order_management.get_order(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict())

@app.route('/get_all_orders', methods=['GET'])
def get_all_orders():
    user_id = request.args.get('user_id')
    order_management = OrderManagement(user_id, "orders")
    orders = order_management.get_all_orders()
    return jsonify([order.to_dict() for order in orders])

@app.route('/update_order', methods=['PUT'])
def update_order():
    user_id = request.form.get('user_id')
    order_id = request.form.get('order_id')
    state = int(request.form.get('state'))
    order_date = datetime.strptime(request.form.get('order_date'), '%Y-%m-%d')
    estimated_arrival_date_str = request.form.get('estimated_arrival_date')
    estimated_arrival_date = datetime.strptime(estimated_arrival_date_str, '%Y-%m-%d')
    
    order_management = OrderManagement(user_id, "orders")
    order = order_management.get_order(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    
    updated_order = OrderWithState(order.id, order.order, state, order_date, estimated_arrival_date)
    order_management.update_order(updated_order)
    
    return jsonify({'message': 'Order updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)
