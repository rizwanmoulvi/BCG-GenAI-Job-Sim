from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

data_df = pd.read_csv('data.csv')

def get_financial_data(company, year, metric):
    try:
        value = data_df.loc[(data_df['Company'].str.lower() == company.lower()) & 
                            (data_df['Fiscal Year'] == year), metric].values[0]
        return value
    except IndexError:
        return None

def generate_response(user_query):
    user_query = user_query.lower()
    
    if "total revenue" in user_query:
        company, year = extract_company_and_year(user_query)
        value = get_financial_data(company, year, 'Total Revenue')
        response = f"The total revenue for {company} in {year} is ${value} Billions."
    elif "net income" in user_query:
        company, year = extract_company_and_year(user_query)
        value = get_financial_data(company, year, 'Net Income')
        response = f"The net income for {company} in {year} is ${value} Billions."
    elif "total assets" in user_query:
        company, year = extract_company_and_year(user_query)
        value = get_financial_data(company, year, 'Total Assets')
        response = f"The total assets for {company} in {year} are ${value} Billions."
    elif "total liabilities" in user_query:
        company, year = extract_company_and_year(user_query)
        value = get_financial_data(company, year, 'Total Liabilities')
        response = f"The total liabilities for {company} in {year} are ${value} Billions."
    elif "cash flow from operation activities" in user_query:
        company, year = extract_company_and_year(user_query)
        value = get_financial_data(company, year, 'Cash Flow From Operation Activities')
        response = f"The cash flow from operation activities for {company} in {year} is ${value} Billions."
    else:
        response = "Sorry, I can only provide information on total revenue, net income, total assets, total liabilities, and cash flow from operation activities."
    
    return response

def extract_company_and_year(query):
    if "microsoft" in query:
        company = "Microsoft"
    elif "apple" in query:  
        company = "Apple"
    else:
        company = "Tesla"  
    year = 2023 #By default, Year can be extracted from query
    for y in range(2021, 2024):
        if str(y) in query:
            year = y
            break
    return company, year

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_query = request.form['query']
        response = generate_response(user_query)
        return render_template('index.html', user_query=user_query, response=response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
