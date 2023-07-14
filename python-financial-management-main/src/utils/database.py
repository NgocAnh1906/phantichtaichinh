import pyodbc


def create_connection():
    server = 'MAIVANTUAN\SQLEXPRESS'
    database = 'FinancialAnalysis'
    username = 'UserPyDB'
    password = '123'

    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=' +
                              server+';DATABASE='+database+';UID='+username+';PWD=' + password)

        return conn
    except Exception as e:
        print("Error connecting to the database:", str(e))
        return None
