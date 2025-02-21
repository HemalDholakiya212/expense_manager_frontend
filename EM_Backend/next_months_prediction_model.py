from db import connection
import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def get_predicted_expense_data(predict_expense):
    conn = connection()
    cursor = conn.cursor()
    final_predicted_expense = None  # Initialize to prevent errors

    try:
        print("From model: ", predict_expense)

        user_id = predict_expense['user_id']
        current_month = predict_expense['current_month']
        current_year = predict_expense['current_year']

        # Fetch required columns only
        expense_query = '''
            SELECT user_id, expense_date, expense_amount 
            FROM em_schema.user_expense 
            WHERE user_id = %s
        '''
        cursor.execute(expense_query, (user_id,))  # Fix tuple issue
        data = cursor.fetchall()

        if not data:
            print("No expense data found for the user.")
            return None

        # Define column names explicitly
        df = pd.DataFrame(data, columns=['user_id', 'expense_date', 'expense_amount'])

        df['expense_date'] = pd.to_datetime(df['expense_date'])
        df['month_year'] = df['expense_date'].dt.to_period('M')

        # Grouping expenses per month
        monthly_totals = df.groupby(['user_id', 'month_year']).agg(
            total_expense=('expense_amount', 'sum')
        ).reset_index()

        # Filter past months' data correctly
        past_months_df = monthly_totals[
            (monthly_totals['month_year'].dt.to_timestamp() <= pd.Timestamp(f"{current_year}-{current_month:02d}-01")) &
            (monthly_totals['user_id'] == user_id)
        ]

        if len(past_months_df) < 3:
            print("Please enter expenses for at least 3 months.")
            return None  # Exit early if not enough data

        print("Total Expenses per Month for Each User:")
        print(past_months_df)

        # Convert decimal.Decimal to float
        expense_list = [float(expense) for expense in past_months_df['total_expense']]
        print("expense list:",expense_list)
        # Fit the model
        model = SimpleExpSmoothing(expense_list).fit(smoothing_level=0.5)

        # Predict next month's expense
        predicted_expense = model.forecast(1)

        final_predicted_expense = round(predicted_expense[0], 2)
        print(f"Predicted expense for next month: {final_predicted_expense:.2f}")

    except Exception as e:
        print("Error:", str(e))

    finally:
        if conn:
            cursor.close()
            conn.close()

    return final_predicted_expense
