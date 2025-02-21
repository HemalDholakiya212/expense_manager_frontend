import psycopg2
import json
import psycopg2.extras
from datetime import datetime
from psycopg2 import OperationalError
from dotenv import load_dotenv

def connection():
    try:
        conn = psycopg2.connect(
            database="expense_manager",
            user='em_user',
            password='123456',
            host='127.0.0.1',
            port='5432'
        )
        print("Connection successful")
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def save_user_signup_details(signup_details):

    conn = connection()
    cursor = conn.cursor()
    print("From db: ", signup_details)
    
    try:
        FETCH_MAX_ID_QUERY = '''
            SELECT COALESCE(MAX(user_id), 0) + 1 AS new_user_id
            FROM em_schema.user_signup
        '''
        cursor.execute(FETCH_MAX_ID_QUERY)
        new_user_id = cursor.fetchone()[0]
        print("New User ID: ", new_user_id)

        INSERT_QUERY = '''
            INSERT INTO em_schema.user_signup(
            user_id,
            first_name,
            last_name,
            email,
            password  
            )   
            VALUES(%s, %s, %s, %s, %s)
        '''
        cursor.execute(INSERT_QUERY, (
            new_user_id,
            signup_details['first_name'],
            signup_details['last_name'],
            signup_details['email'],
            signup_details['password']
        ))
        conn.commit()
        return {"status": "success", "message": "User registered successfully."}

    except Exception as e:
        print("Error occurred:", str(e))
        return {"status": "error", "message": f"An error occurred while saving user: {str(e)}"}

    finally:
        if conn:
            cursor.close()
            conn.close()

def attempt_to_signin_for_user(login_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    valid_user = False
    try:
        print("From db:",login_data)

        QUERY = ''' 
                SELECT user_id,first_name,last_name,email, password FROM em_schema.user_signup
                WHERE email = '{}' 
                '''.format(login_data['email'])

        cursor.execute(QUERY)
        reg_records = cursor.fetchall()
        print("reg_records: ",reg_records)

        if reg_records:
            for row in reg_records:
                user_password = row['password']
                email = row['email']
                first_name = row['first_name']
                last_name = row['last_name']
                user_id = row['user_id']

            print(user_password,email,first_name,last_name,user_id)

            if (login_data['email'] == email and 
                login_data['password'] == user_password):
                valid_user = True

                user_info = {
                    'user_id': user_id,
                    'first_name': first_name,
                    'last_name': last_name
                }

    except Exception as e:
        print("Error", str(e), "Occurred")

    finally:
        if conn:
            cursor.close()
            conn.close()
    return valid_user,user_info

def save_user_expense(expense_details):

    conn = connection()
    cursor = conn.cursor()
    print("From db: ", expense_details)
    
    try:
        FETCH_MAX_ID_QUERY = '''
            SELECT COALESCE(MAX(expense_id), 0) + 1 AS new_expense_id
            FROM em_schema.user_expense
        '''
        cursor.execute(FETCH_MAX_ID_QUERY)
        new_expense_id = cursor.fetchone()[0]
        print("New User ID: ", new_expense_id)

        INSERT_QUERY = '''
            INSERT INTO em_schema.user_expense(
            expense_id,
            user_id,
            expense_amount,
            expense_category,
            expense_description,
            expense_date
            )   
            VALUES(%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(INSERT_QUERY, (
            new_expense_id,
            expense_details['user_id'],
            expense_details['expense_amount'],
            expense_details['expense_category'],
            expense_details['expense_description'],
            expense_details['expense_date'],
        ))
        conn.commit()
        return {"status": "success", "message": "User registered successfully."}

    except Exception as e:
        print("Error occurred:", str(e))
        return {"status": "error", "message": f"An error occurred while saving user: {str(e)}"}

    finally:
        if conn:
            cursor.close()
            conn.close()

def save_user_budget(budget_details):

    conn = connection()
    cursor = conn.cursor()
    print("From db: ", budget_details)
    
    try:
        FETCH_MAX_ID_QUERY = '''
            SELECT COALESCE(MAX(budget_id), 0) + 1 AS new_expense_id
            FROM em_schema.user_budget
        '''
        cursor.execute(FETCH_MAX_ID_QUERY)
        new_budget_id = cursor.fetchone()[0]
        print("New User ID: ", new_budget_id)

        INSERT_QUERY = '''
            INSERT INTO em_schema.user_budget(
            budget_id,
            user_id,
            budget_amount,
            budget_category
            )   
            VALUES(%s, %s, %s, %s)
        '''
        cursor.execute(INSERT_QUERY, (
            new_budget_id,
            budget_details['user_id'],
            budget_details['budget_amount'],
            budget_details['budget_category']
        ))
        conn.commit()
        return {"status": "success", "message": "User registered successfully."}

    except Exception as e:
        print("Error occurred:", str(e))
        return {"status": "error", "message": f"An error occurred while saving user: {str(e)}"}

    finally:
        if conn:
            cursor.close()
            conn.close()


def fetch_expense_chart_data(fetch_expense_details):
    selected_month_raw = fetch_expense_details.get('selected_month')
    selected_month = str(selected_month_raw).zfill(2) if selected_month_raw is not None else None
    print("Selected Month (2-digit):", selected_month)

    conn = connection()
    cursor = conn.cursor()
    try:
        # Initialize the expense query
        query1 = '''SELECT expense_category, SUM(expense_amount) as total 
                    FROM em_schema.user_expense 
                    WHERE user_id = %s 
                    AND EXTRACT(YEAR FROM expense_date) = %s'''

        # If the month is provided, add an additional condition for the month
        if selected_month is not None:
            query1 += " AND EXTRACT(MONTH FROM expense_date) = %s"

        query1 += " GROUP BY expense_category"

        # Execute the expenses query
        expense_params = [fetch_expense_details['user_id'], fetch_expense_details['selected_year']]
        if selected_month is not None:
            expense_params.append(selected_month)

        cursor.execute(query1, expense_params)
        expense_rows = cursor.fetchall()

        # Initialize the budget query
        query2 = '''SELECT budget_category, SUM(budget_amount) as total 
                    FROM em_schema.user_budget 
                    WHERE user_id = %s 
                    AND EXTRACT(YEAR FROM created_at) = %s'''

        # If the month is provided, add an additional condition for the month
        if selected_month is not None:
            query2 += " AND EXTRACT(MONTH FROM created_at) = %s"

        query2 += " GROUP BY budget_category"

        # Execute the budget query
        budget_params = [fetch_expense_details['user_id'], fetch_expense_details['selected_year']]
        if selected_month is not None:
            budget_params.append(selected_month)

        cursor.execute(query2, budget_params)
        budget_rows = cursor.fetchall()

        # Convert database rows into dictionaries
        expense_data = [{"category": row[0], "expense_amount": row[1]} for row in expense_rows]
        budget_data = [{"category": row[0], "budget_amount": row[1]} for row in budget_rows]

        # Merge expenses and budgets by category
        merged_data = []

        # Add expense data with matching or zero budget
        for expense in expense_data:
            category = expense["category"]
            matching_budget = next((budget for budget in budget_data if budget["category"] == category), None)
            merged_data.append({
                "category": category,
                "expense_amount": expense["expense_amount"],
                "budget_amount": matching_budget["budget_amount"] if matching_budget else 0
            })

        # Add budget data not in expense data
        for budget in budget_data:
            if not any(item["category"] == budget["category"] for item in merged_data):
                merged_data.append({
                    "category": budget["category"],
                    "expense_amount": 0,
                    "budget_amount": budget["budget_amount"]
                })

        print("Merged Data:", merged_data)

        # Prepare the table query
        tableQuery = '''WITH expense_data AS (
                            SELECT 
                                user_id,
                                expense_category,
                                SUM(expense_amount) AS total_expense
                            FROM 
                                em_schema.user_expense
                            WHERE 
                                user_id = %s 
                                AND TO_CHAR(expense_date, 'YYYY-MM') = %s
                            GROUP BY 
                                user_id, expense_category
                        ),
                        budget_data AS (
                            SELECT 
                                user_id,
                                budget_category,
                                SUM(budget_amount) AS total_budget
                            FROM 
                                em_schema.user_budget
                            WHERE 
                                user_id = %s 
                                AND TO_CHAR(created_at, 'YYYY-MM') = %s
                            GROUP BY 
                                user_id, budget_category
                        )
                        SELECT 
                            COALESCE(b.user_id, e.user_id) AS user_id,
                            COALESCE(b.budget_category, e.expense_category) AS category,
                            COALESCE(e.total_expense, 0) AS total_expense,
                            COALESCE(b.total_budget, 0) AS total_budget,
                            COALESCE(b.total_budget, 0) - COALESCE(e.total_expense, 0) AS saving
                        FROM 
                            budget_data b
                        FULL OUTER JOIN 
                            expense_data e ON b.user_id = e.user_id AND b.budget_category = e.expense_category
                        ORDER BY 
                            category;'''

        # Execute the table query
        table_params = [
            fetch_expense_details['user_id'], 
            f"{fetch_expense_details['selected_year']}-{selected_month}" if selected_month else f"{fetch_expense_details['selected_year']}-01",
            fetch_expense_details['user_id'], 
            f"{fetch_expense_details['selected_year']}-{selected_month}" if selected_month else f"{fetch_expense_details['selected_year']}-01"
        ]
        
        cursor.execute(tableQuery, table_params)
        table_rows = cursor.fetchall()

        table_data = [{"category": row[1], "expense_amount": row[2], "budget_amount": row[3], "saving": row[4]} for row in table_rows]
        print("Table Data:", table_data)

    except Exception as e:
        print("Error", str(e), "Occurred")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return merged_data, table_data


def get_expense_budget_data(fetch_expense_details):
    conn = connection()
    cursor = conn.cursor()
    try:
        # Initialize the query parts
        budget_query = '''SELECT user_id, SUM(budget_amount) AS total_budget 
                          FROM em_schema.user_budget 
                          WHERE user_id = %s '''

        expense_query = '''SELECT user_id, SUM(expense_amount) AS total_expense 
                           FROM em_schema.user_expense 
                           WHERE user_id = %s '''

        # Check if selected_year is provided
        if fetch_expense_details['selected_year'] is not None:
            budget_query += ''' AND EXTRACT(YEAR FROM created_at) = %s '''
            expense_query += ''' AND EXTRACT(YEAR FROM expense_date) = %s '''
            
            # Add month filter if selected_month is provided
            if fetch_expense_details['selected_month'] is not None:
                budget_query += ''' AND EXTRACT(MONTH FROM created_at) = %s '''
                expense_query += ''' AND EXTRACT(MONTH FROM expense_date) = %s '''
        
        # Finalize the queries
        budget_query += ''' GROUP BY user_id '''
        expense_query += ''' GROUP BY user_id '''

        # Execute the budget query
        budget_params = [fetch_expense_details['user_id']]
        if fetch_expense_details['selected_year'] is not None:
            budget_params.append(fetch_expense_details['selected_year'])
        if fetch_expense_details['selected_month'] is not None:
            budget_params.append(fetch_expense_details['selected_month'])

        cursor.execute(budget_query, budget_params)
        budget_rows = cursor.fetchall()

        # Execute the expense query
        expense_params = [fetch_expense_details['user_id']]
        if fetch_expense_details['selected_year'] is not None:
            expense_params.append(fetch_expense_details['selected_year'])
        if fetch_expense_details['selected_month'] is not None:
            expense_params.append(fetch_expense_details['selected_month'])

        cursor.execute(expense_query, expense_params)
        expense_rows = cursor.fetchall()

        # Prepare the final data output
        total_budget = budget_rows[0][1] if budget_rows else 0  # Assuming user_id is unique
        total_expense = expense_rows[0][1] if expense_rows else 0

        data = [{"total_budget": total_budget, "total_expense": total_expense}]
        print("From DB rows:", data)

    except Exception as e:
        print("Error occurred:", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return data

def get_month_comparison_data(compare_months):

    selecte_month1 = compare_months.get('month1')
    month1 = str(selecte_month1).zfill(2) if selecte_month1 is not None else None
    selecte_month2 = compare_months.get('month2')
    month2 = str(selecte_month2).zfill(2) if selecte_month1 is not None else None
    
    conn = connection()
    cursor = conn.cursor()

    try:

        QUERY_month1 = ''' 
                SELECT sum(expense_amount) as total_expense FROM em_schema.user_expense
                WHERE user_id = '{}' AND TO_CHAR(expense_date, 'YYYY') = '{}' AND TO_CHAR(expense_date, 'MM')='{}'
                '''.format(
                    compare_months['user_id'],
                    compare_months['year'],
                    month1
                    )

        cursor.execute(QUERY_month1)
        reg_records1 = cursor.fetchall()
        print("reg_records: ",reg_records1)
        month1_expense = reg_records1[0][0]

        QUERY_month2 = ''' 
                SELECT sum(expense_amount) as total_expense FROM em_schema.user_expense
                WHERE user_id = '{}' AND TO_CHAR(expense_date, 'YYYY') = '{}' AND TO_CHAR(expense_date, 'MM')='{}'
                '''.format(
                    compare_months['user_id'],
                    compare_months['year'],
                    month2
                    )

        cursor.execute(QUERY_month2)
        reg_records2 = cursor.fetchall()
        print("reg_records: ",reg_records2[0])
        month2_expense = reg_records2[0][0]
 
        months_data = {
                    'month1':month1,
                    'month2':month2,
                    'month1_expense': month1_expense,
                    'month2_expense': month2_expense,
                    
                }
        print("months_data:",months_data)

    except Exception as e:
        print("Error", str(e), "Occurred")

    finally:
        if conn:
            cursor.close()
            conn.close()
    return months_data




    

