import requests
import uuid

# API Endpoint and Headers
url = "https://pfe-apigw-uat.porter.in/v1/orders/create"
headers = {
    "x-api-key": "8c18d7ac-38a8-4930-a020-149b0fdf45d5",
    "Content-Type": "application/json"
}

payload = {
    "request_id": "123e4567",
    "delivery_instructions": {
        "instructions_list": [
            {
                "type": "text",
                "description": "handle with care"
            }
        ]
    },
    "pickup_details": {
        "address": {
            "apartment_address": "27",
            "street_address1": "Sona Towers",
            "street_address2": "Krishna Nagar Industrial Area",
            "landmark": "Hosur Road",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560029",
            "country": "India",
            "lat": 12.935025,
            "lng": 77.609261,
            "contact_details": {
                "name": "Test Sender",
                "phone_number": "+919959463811"
            }
        }
    },
    "drop_details": {
        "address": {
            "apartment_address": "Apartment 12",
            "street_address1": "BTM Layout",
            "street_address2": "Order ID here",
            "landmark": "BTM Layout Landmark",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560029",
            "country": "India",
            "lat": 12.947146,
            "lng": 77.62103,
            "contact_details": {
                "name": "Test Receiver",
                "phone_number": "+919959463811"
            }
        }
    },
    "additional_comments": "This is a test comment"
}

# Make the API Request
try:
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code == 201:
        print("Order Created Successfully!")
        print("Response:", response_data)
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response_data)
except Exception as e:
    print(f"An error occurred: {e}")
