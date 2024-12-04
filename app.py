from flask import Flask, request
from dbconn import insert_order_update,fetch_record,store_order_details
import requests

# Flask application setup
app = Flask(__name__)

@app.route('/')
def index():
    return 'service are up'

@app.route('/porter/createorder', methods=['POST'])
def createorder():
    try:
        data = request.json
        query = F"SELECT * FROM Porter_delivery_Address WHERE request_id = '{data['request_id']}'"
        result = fetch_record(query)
        print(result)
        if result['status']:
            result= result['result']
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

            # API Endpoint and Headers
            url = "https://pfe-apigw-uat.porter.in/v1/orders/create"
            headers = {
                "x-api-key": "8c18d7ac-38a8-4930-a020-149b0fdf45d5",
                "Content-Type": "application/json"
            }

            # Make the API Request
            try:
                response = requests.post(url, json=json_data, headers=headers)
                result = response.json()

                if response.status_code == 201:
                    print("Order Created Successfully!")
                    print("Response:", result)
                    store_order_details(result)
                else:
                    print(f"Error: {response.status_code}")
                    print("Response:", result)
            except Exception as e:
                print(f"An error occurred: {e}")
        return result

    except Exception as e:
        # If an error occurs, respond with an error message
        print(f"Error: {e}")
        return 'Failed to process webhook', 500


# Define the route to receive webhooks
@app.route('/porter/order_update', methods=['POST'])
def order_update():
    try:
        # Get the JSON data from the webhook
        webhook_data = request.json
        # Check status and insert data based on status type
        if webhook_data['status'] == 'order_accepted':
            insert_order_update(webhook_data,webhook_data['status'])
        elif webhook_data['status'] == 'order_start_trip':
            insert_order_update(webhook_data,webhook_data['status'])
        elif webhook_data['status'] == 'order_end_job':
            insert_order_update(webhook_data,webhook_data['status'])
        elif webhook_data['status'] == 'order_cancel':
            insert_order_update(webhook_data,webhook_data['status'])
        elif webhook_data['status'] == 'order_reopen':
            insert_order_update(webhook_data,webhook_data['status'])

        # Respond with a success message
        return 'Webhook received and saved to database', 200
    except Exception as e:
        # If an error occurs, respond with an error message
        print(f"Error: {e}")
        return 'Failed to process webhook', 500

if __name__ == '__main__':
    app.run(debug=True)
