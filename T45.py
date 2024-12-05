import requests

# API details
url = "https://pfe-apigw-uat.porter.in/v1/simulation/initiate_order_flow"
headers = {
    "X-API-KEY": "8c18d7ac-38a8-4930-a020-149b0fdf45d5",
    "Content-Type": "application/json"
}
payload = {
    "order_id": "CRN1733381794037",
    "flow_type": 0
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)

# Output response
if response.status_code == 200:
    print("Order flow initiated successfully.")
    print(response.json())
else:
    print(f"Failed with status code {response.status_code}")
    print(response.json())
