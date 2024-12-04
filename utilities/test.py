import requests

# Base URL (change to production if needed)
BASE_URL = "https://pfe-apigw-uat.porter.in/v1/get_quote"

# API token for authentication (replace with your actual token)
API_TOKEN = "8c18d7ac-38a8-4930-a020-149b0fdf45d5"

# Define request payload
payload = {
    "pickup_details": {
        "lat": 12.935025018880504,
        "lng": 77.6092605236106
    },
    "drop_details": {
        "lat": 12.947146336879577,
        "lng": 77.62102993895199
    },
    "customer": {
        "name": "salik",
        "mobile": {
            "country_code": "+91",
            "number": "7678139714"
        }
    }
}

# Define headers
headers = {
    "X-API-KEY": API_TOKEN,
    "Content-Type": "application/json"
}

try:
    # Send GET request
    response = requests.get(BASE_URL, json=payload, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        print("Success Response:")
        print(response.json())
    else:
        print(f"Error {response.status_code}:")
        print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
