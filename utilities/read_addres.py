import mysql.connector
import json

db_config = {'host': 'MYSQL5048.site4now.net','user': 'a50d85_payroll', 'password': 'p3r3nnial','database': 'db_a50d85_payroll'  }

# Database connection
db = mysql.connector.connect(**db_config
                        )

cursor = db.cursor(dictionary=True)  # Use dictionary cursor for key-value pairs

# Define the request_id you want to query
request_id = '123e4567'

# Query to fetch data based on request_id
query = "SELECT * FROM Porter_delivery_Address WHERE request_id = %s"
cursor.execute(query, (request_id,))
result = cursor.fetchone()

if result:
    # Map database fields to JSON structure
    json_data = {
        "request_id": result["request_id"],
        "delivery_instructions": {
            "instructions_list": [
                {
                    "type": "text",
                    "description": result["instructions_text"]
                }
            ]
        },
        "pickup_details": {
            "address": {
                "apartment_address": result["pickup_apartment_address"],
                "street_address1": result["pickup_street_address1"],
                "street_address2": result["pickup_street_address2"],
                "landmark": result["pickup_landmark"],
                "city": result["pickup_city"],
                "state": result["pickup_state"],
                "pincode": result["pickup_pincode"],
                "country": result["pickup_country"],
                "lat": result["pickup_lat"],
                "lng": result["pickup_lng"],
                "contact_details": {
                    "name": result["pickup_contact_name"],
                    "phone_number": result["pickup_contact_phone"]
                }
            }
        },
        "drop_details": {
            "address": {
                "apartment_address": result["drop_apartment_address"],
                "street_address1": result["drop_street_address1"],
                "street_address2": result["drop_street_address2"],
                "landmark": result["drop_landmark"],
                "city": result["drop_city"],
                "state": result["drop_state"],
                "pincode": result["drop_pincode"],
                "country": result["drop_country"],
                "lat": result["drop_lat"],
                "lng": result["drop_lng"],
                "contact_details": {
                    "name": result["drop_contact_name"],
                    "phone_number": result["drop_contact_phone"]
                }
            }
        },
        "additional_comments": result["additional_comments"]
    }

    # Print the JSON in a formatted manner
    print(json.dumps(json_data, indent=4))
else:
    print(f"No data found for request_id: {request_id}")

# Close the connection
cursor.close()
db.close()
