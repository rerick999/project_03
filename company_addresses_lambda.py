# this is the lambda that queries the database for all the company addresses

import json
import mysql.connector

def lambda_handler(event, context):
    myhost = 'finance-database-1-mysql.cgmm17eujq52.us-west-2.rds.amazonaws.com'
    mydatabase = 'myfinancedb'
    myuser = '' # login goes here
    mypassword = '' # password goes here

    try:
        connection = mysql.connector.connect(
            host=myhost,
            database=mydatabase,
            user=myuser,
            password=mypassword
        )

        cursor = connection.cursor()

        query = "SELECT * FROM company_addresses"
        cursor.execute(query)

        results = cursor.fetchall()

        rows = []
        for row in results:
            rows.append(row)

        json_str = json.dumps(rows)


        with open('/tmp/rows.json', 'w') as file:
            file.write(json_str)

        with open('/tmp/rows.json', 'r') as file:
            file_contents = file.read()

        data = json.loads(file_contents)

        return {
            'statusCode': 200,
            'body': data
        }

    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()