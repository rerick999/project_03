import json
import mysql.connector

def lambda_handler(event, context):
    myhost = 'finance-database-1-mysql.cgmm17eujq52.us-west-2.rds.amazonaws.com'
    mydatabase = 'myfinancedb'
    myuser = 'admin'
    mypassword = 'abc123ABC'

    cursor = None  # Initialize cursor variable
    connection = None  # Initialize connection variable

    try:
        ticker = event['queryStringParameters'].get('ticker')

        if not ticker:
            return {
                'statusCode': 400,
                'body': 'Ticker parameter is missing'
            }

        connection = mysql.connector.connect(
            host=myhost,
            database=mydatabase,
            user=myuser,
            password=mypassword
        )

        cursor = connection.cursor()

        query = f"SELECT ticker, DATE_FORMAT(date, '%Y-%m-%d') AS date_recorded, sector, 52WeekChange, 52WeekHigh, 52WeekLow, ask, bid, dailyOpen, previousClose, dailyVolume, quickRatio, 10DayAverageVolume, marketCap FROM stock_data WHERE ticker = '{ticker}'"
        cursor.execute(query)

        results = cursor.fetchall()

        rows = []
        for row in results:
            rows.append(row)

        # Convert the list of rows to JSON string
        json_str = json.dumps(rows)

        # Write JSON string to a file
        with open('/tmp/rows.json', 'w') as file:
            file.write(json_str)

        # Read the file contents
        with open('/tmp/rows.json', 'r') as file:
            file_contents = file.read()

        # Deserialize the JSON string to a Python object
        data = json.loads(file_contents)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(data)
        }

    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
