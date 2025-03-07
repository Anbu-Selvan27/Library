import pyodbc

server = 'ANBU-PC\SQLEXPRESS' 
database = 'book'
driver = '{ODBC Driver 17 for SQL Server}'  

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
    # Perform database operations here...
    conn.close()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Connection failed: {sqlstate}")