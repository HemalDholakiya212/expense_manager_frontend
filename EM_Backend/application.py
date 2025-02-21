from fastapi import FastAPI
import db as db
import json
import schemas
from fastapi.responses import JSONResponse
import base64
import io
import pandas as pd
from PIL import Image
import pytesseract
from google.cloud import vision
import os
from dotenv import load_dotenv
import re
import jsonify
from nltk.tokenize import word_tokenize
import next_months_prediction_model as model

app = FastAPI()

from fastapi.responses import JSONResponse

@app.post("/save_user_signup_details")
def save_user_signup_details(signup_details: schemas.UserSignup):
    result = db.save_user_signup_details(signup_details.dict())
    
    if result["status"] == "success":
        return JSONResponse(content=result, status_code=200) 
    else:
        return JSONResponse(content=result, status_code=400)

@app.post("/attempt_to_signin_for_user")
def attempt_to_signin_for_user(login_data:schemas.LoginForUser):
    print("From backend application.py:",login_data)
    valid_user_login = ""
    valid_user,user_info= db.attempt_to_signin_for_user(login_data.dict())
    if(valid_user):
        valid_user_login = "Login Successful"
    else:
        valid_user_login = "Login Failed"
        user_name = None

    response = {
        "email" :login_data.email,
        "status" : valid_user_login,
        "first_name": user_info['first_name'],
        "last_name": user_info['last_name'],
        "user_id": user_info['user_id'],
    }

    print("Response:",response)
    return JSONResponse(content=response, status_code=200)

@app.post("/save_user_expense")
def save_user_expense(expense_details: schemas.UserExpense):
    result = db.save_user_expense(expense_details.dict())
    print("Result save: ",expense_details)
    
    if result["status"] == "success":
        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content=result, status_code=400)
    
@app.post("/save_user_budget")
def save_user_budget(budget_details: schemas.UserBudget):
    print(budget_details)
    result = db.save_user_budget(budget_details.dict())
    
    if result["status"] == "success":
        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content=result, status_code=400)

@app.post("/get_user_expense_chart_data")
def get_user_expense_chart_data(fetch_expense_details: schemas.FetchExpenseData):
    result = db.fetch_expense_chart_data(fetch_expense_details.dict())
    print("expense result: ",result)
    return result

@app.post("/save_receipt")
def save_receipt(receipt: schemas.UploadReceipt):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Read file contents (base64 encoded string)
    file_contents = receipt.receipt
    
    # Decode the base64 string to bytes
    image_data = base64.b64decode(file_contents)
    
    # Create a BytesIO object from the decoded data
    image = Image.open(io.BytesIO(image_data))
    
    # Perform OCR on the image
    extracted_data = pytesseract.image_to_string(image)
    print("extracted_data:",extracted_data)

    result = extract_receipt_details(extracted_data)
    print("Result: ",result)

    return result

def extract_receipt_details(extracted_data):

    tokens = word_tokenize(extracted_data)

    cleaned_tokens = [re.sub(r'[~`!@#%^&*()_=+;:?><]', '', word) for word in tokens]
    number_tokens = [re.sub(r'[a-zA-Z~`!@#%^&*()_=+;:?><,[]|\/.-''""]', '', word) for word in tokens]
    cleaned_data = ' '.join(cleaned_tokens)
    print("Cleaned Data:", cleaned_data)
    print("Number Token:", number_tokens)
    numbers = [number for number in number_tokens if number.strip()]
    amount_tokens = ' '.join(numbers)
    print(amount_tokens)

    result = {}
    
    date_match = re.search(r'\d{1,2}[-/](\d{1,2}|[a-zA-Z]{3})[-/]\d{2,4}', cleaned_data)
    if date_match:
        date_str = date_match.group()
        date = date_str
        result['Date'] = date
    else:
        date = None

    amount_match = re.findall(r'\b\d+\.\d{1,2}\b', amount_tokens)
    amounts = [float(amount) for amount in amount_match]
    print("Amounts:",amounts)

    if amounts:
        max_amount = max(amounts)
        print("Maximum Amount:", max_amount)
        result['Amount']=max_amount

    else:
        expense_amount = None

    description_match = re.search(r'\d+\s+([A-Z0-9\s\.\-]+)', extracted_data)
    if description_match:
        description_data = description_match.group()
        description = description_data
        result['Description']=description
    else:
        description = None

    categories = {
        'Clothing': ['garments','clothing', 'apparel', 'fashion', 'shoe', 'dress', 'PUMA', 'Nike', 'Adidas','shirt','pent'],
        'Groceries': ['grocery', 'supermarket', 'food', 'market', 'fruit', 'vegetable'],
        'Utilities': ['electricity', 'water', 'gas', 'utility', 'bill'],
        'Entertainment': ['movie', 'dinner', 'concert', 'event', 'entertainment'],
        'Sports': ['sports', 'equipment', 'gear'],
        'Other': []
    }

    # Initialize a variable to hold the category
    category = 'Other'  # Default category

    # Search for keywords in the receipt data to determine the category
    if extracted_data:
        for cat, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in extracted_data.lower():
                    category = cat
                    print(f"Matched {keyword} for category: {cat}")
                    break  # Exit the inner loop if a match is found
            if category != 'Other':  # Stop checking if a category has been matched
                break

    category_data = category
    result['Category']=category_data

    return result

@app.post("/get_expense_and_budget_data")
def get_expense_and_budget_data(fetch_expense_details: schemas.FetchExpenseData):
    print("expense result: ",fetch_expense_details)
    result = db.get_expense_budget_data(fetch_expense_details.dict())
    print(result)
    return result

@app.post("/get_month_comparison_data")
def get_month_comparison_data(compare_months: schemas.CompareMonths):
    print("compare months:",compare_months)
    result = db.get_month_comparison_data(compare_months.dict())
    print("expense result: ",result)
    return result

@app.post("/get_predicted_expense_data")
def get_predicted_expense_data(predict_expense: schemas.PredictExpense):
    print("compare months:",predict_expense)
    result = model.get_predicted_expense_data(predict_expense.dict())
    print("expense result: ",result)
    return result

    

                                         
