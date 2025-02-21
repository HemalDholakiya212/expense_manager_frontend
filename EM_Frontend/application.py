from flask import Flask,render_template,request,url_for,jsonify,json,session,redirect
from flask_cors import CORS,cross_origin
import json
import pandas as pd
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import base64

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  #Cookie Same site attribute
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = 'This_is_very_secret'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        # self.username = username

@login_manager.user_loader
def load_user(email):
    if email:
        return User(email)
    return None


@app.route('/homepage')
def homepage():
    return render_template('homePage.html')

def get_logged_in_user():
    user_login = False
    user_info = session.get('email')
    if(user_info is not None):
        user_logged_in = user_info
    else:
        user_logged_in = None
    if(user_logged_in is not None):
        user_login = True

    return user_login

@app.route('/dashboard')
@login_required
def dashBoard():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    print('Logged in user',user_info)
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    print("first_name: ",first_name,"last_name: ",last_name)
    return render_template('dashBoard.html',user_login=user_login,first_name=first_name,last_name=last_name)

@app.route('/signup')
def signup():
    return render_template('signUp.html')

@app.route('/signin')
def signin():
    
    return render_template('signIn.html')

@app.route('/addexpense')
@login_required
def addexpense():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    return render_template('addExpense.html',user_login=user_login)

@app.route('/addbudget')
@login_required
def addbudget():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    return render_template('addBudget.html',user_login=user_login)

@app.route('/addreceipt')
@login_required
def addreceipt():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    # amount = session.get('Amount')
    return render_template('addReceipt.html',user_login=user_login)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    user_login = get_logged_in_user()
    return render_template('homePage.html',user_login = user_login)

def get_service_url():
    return 'http://localhost:30000'

def post_api_function(url, data):
    response = ''
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

from flask import jsonify

@app.route('/user_signup', methods=['POST'])
def user_signup():
    url = get_service_url() + '/save_user_signup_details'
    request_data = request.json
    print("Request Data:", request_data)
    
    try:
        # Call the post_api_function to send the request to the backend
        response = post_api_function(url, request_data)

        # Check if the response is valid and return it
        if response is not None and response.ok:
            return jsonify(response.json()), response.status_code  # Assuming response.json() returns a dict
        else:
            return jsonify({"status": "error", "message": "Failed to save user details."}), 400
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": "An internal error occurred."}), 500

@app.route('/user_signin', methods=['POST'])
def user_signin():
    url = get_service_url() + '/attempt_to_signin_for_user'
    request_data = request.json
    response = post_api_function(url, request_data)
    result = response.json()
    if(result['status'] == 'Login Failed'):
       print("Login Failed")
    else:
        email = result.get('email')
        first_name = result.get('first_name')
        last_name = result.get('last_name')
        user_id = result.get('user_id')
        user = User(email)  
        login_user(user) 
        session['email'] = email
        session['first_name'] = first_name
        session['last_name'] = last_name 
        session['user_id'] = user_id 
        print("Logged in successfully: ", session['email'],"User Id: ",session['user_id'])
    return jsonify(result)

@app.route('/user_expense', methods=['POST'])
def user_expense():
    url = get_service_url() + '/save_user_expense'
    request_data = request.json
    print("Request Data user expense:", request_data)
    
    try:
        response = post_api_function(url, request_data)

        if response is not None and response.ok:
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"status": "error", "message": "Failed to save user details."}), 400
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": "An internal error occurred."}), 500

@app.route('/get_user_expense_chart', methods=['POST'])
def get_user_expense_chart():
    url = get_service_url() + '/get_user_expense_chart_data'
    request_data = request.json
    response = post_api_function(url, request_data)
    result = response.json()
    print("expense result: ",result)
   
    return jsonify(result)

@app.route('/user_budget', methods=['POST'])
def user_budget():
    request_data = request.json
    print("Request Data:",request_data)
    url = get_service_url() + '/save_user_budget'
    
    try:
        response = post_api_function(url, request_data)

        if response is not None and response.ok:
            return jsonify(response.json()), response.status_code 
        else:
            return jsonify({"status": "error", "message": "Failed to save user details."}), 400
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": "An internal error occurred."}), 500


@app.route('/upload_receipt', methods=['POST'])
def upload_receipt(): 
    if 'receipt' not in request.files:
        return jsonify({'error': 'No receipt file found in the request'}), 400

    receipt_file = request.files['receipt']
    print("from application.py:",receipt_file)

    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is missing'}), 400

    try:
        receipt_data = receipt_file.read()
        base64_receipt = base64.b64encode(receipt_data).decode('utf-8')
        print(f"Encoded Base64 Receipt: {base64_receipt[:100]}...")  

        request_data = {
            "receipt": base64_receipt,
            "user_id": user_id
        }

        url = get_service_url() + '/save_receipt'
        response = post_api_function(url, request_data)
        response_data = response.json()
        print("Response data:",response_data)

        if isinstance(response, dict) and "error" in response:
            return jsonify(response), 500

        return jsonify(response_data), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_expense_and_budget', methods=['POST'])
def get_expense_and_budget():

    url = get_service_url() + '/get_expense_and_budget_data'
    request_data = request.json
    print("get_expense_and_budget:",request_data)

    response = post_api_function(url, request_data)
    
    result = response.json()
    print("expense result: ",result)
   
    return jsonify(result)

@app.route('/get_month_comparison',methods=["POST"])
def get_month_comparison():
    url = get_service_url()+'/get_month_comparison_data'
    request_data = request.json
    print("month comparison:",request_data)

    response = post_api_function(url,request_data)

    result = response.json()
    print(result)
    return jsonify(result)


@app.route('/get_predicted_expense', methods=['POST'])
def get_predicted_expense():

    url = get_service_url() + '/get_predicted_expense_data'
    request_data = request.json
    print("get_expense_and_budget:",request_data)

    response = post_api_function(url, request_data)
    
    result = response.json()
    print("expense result: ",result)
   
    return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
