from flask import Flask, request,jsonify
from dbconn import insert_webhook_payload,fetch_record,store_order_details,db_createorder
import requests
import random
import string

# Flask application setup
app = Flask(__name__)

# Generate random request_id
def generate_request_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

@app.route('/save_order_address', methods=['POST'])
def save_order_address():
    try:
        # Get JSON data from the request
        order_data = request.get_json()

        # Generate a random request_id
        request_id = generate_request_id()

        data = db_createorder(order_data,request_id)
        if data['status']:
            return jsonify(data), 200
        else:
            return jsonify(data), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/')
def index():
    return 'service are up'

PFE_API_GW_URL = 'https://pfe-apigw-uat.porter.in/'
API_KEY = '8c18d7ac-38a8-4930-a020-149b0fdf45d5'
@app.route('/order/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    try:
        # Construct the API URL
        url = f"{PFE_API_GW_URL}v1/orders/{order_id}/cancel"

        # Headers for the API call
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        # Pass the request body from the Flask client to the external API
        payload = request.json if request.is_json else {}

        # Make the POST request to cancel the order
        response = requests.post(url, headers=headers, json=payload)

        # Handle successful response
        if response.status_code in [200, 204]:
            return jsonify({
                "message": "Order canceled successfully.",
                "response": response.json() if response.content else {}
            }), response.status_code
        else:
            # Handle API errors
            return jsonify({
                "error": "Failed to cancel the order.",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": "An error occurred while processing your request.", "details": str(e)}), 500

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        url = f'{PFE_API_GW_URL}v1/orders/'
        # Construct the API URL
        url = f"{url}{order_id}"

        # Headers for the API call
        headers = {
            "x-api-key": f'{API_KEY}'
        }

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check for a successful response
        if response.status_code == 200:
            # Return the JSON response from the external API
            return jsonify(response.json()), 200
        else:
            # Handle API errors
            return jsonify({
                "error": "Failed to fetch the order details.",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": "An error occurred while processing your request.", "details": str(e)}), 500




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
            url = F"{PFE_API_GW_URL}v1/orders/create"
            headers = {
                "x-api-key": f"{API_KEY}",
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
                    return result
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
        insert_webhook_payload(webhook_data)

        # Respond with a success message
        return 'Webhook received and saved to database', 200
    except Exception as e:
        # If an error occurs, respond with an error message
        print(f"Error: {e}")
        return 'Failed to process webhook', 500

if __name__ == '__main__':
    app.run()
