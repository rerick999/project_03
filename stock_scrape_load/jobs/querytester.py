import config
import mysql.connector

ticker = 'msft'
result_count = 1

query = f"select * from stock_data where ticker = '{ticker}' order by date desc limit {result_count}"

try:
    connection = mysql.connector.connect(
        host=config.myhost,
        database=config.mydatabase,
        user=config.myuser,
        password=config.mypassword
        )
    
    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    print(results)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()