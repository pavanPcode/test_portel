import pandas as pd
import requests
import time
import random
import string

# Function to generate random order IDs
def generate_request_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to send a POST request
def send_order_update(order_data):
    url = "https://testporter.azurewebsites.net/porter/order_update"
    response = requests.post(url, json=order_data)
    if response.status_code == 200:
        print(f"Order {order_data['order_id']} updated successfully")
    else:
        print(f"Failed to update order {order_data['order_id']}")

# Read the Excel file
excel_file = 'Book1.xlsx'  # Replace with your actual file path
df = pd.read_excel(excel_file)

# Loop through each row and send POST requests based on order status
for index, row in df.iterrows():
    order_data = {}

    # Order ID
    order_data['order_id'] = row['Order ID']

    # Event timestamp
    order_data['event_ts'] = row['Event Timestamp']

    # Common order details
    order_details = {
        'partner_location': {
            'lat': row['Latitude'],
            'long': row['Longitude']
        }
    }

    # Based on the status, create the appropriate JSON data
    if row['Status'] == 'order_accepted':
        order_data = {
            "status": "order_accepted",
            "order_id": row['Order ID'],
            "order_details":
                {
                    "event_ts": row['Event Timestamp'],
                    "partner_location":
                        {
                            "lat": row['Latitude'],
                            "long": row['Longitude']
                        },
                    "driver_details":
                        {
                            "driver_name": row['Driver Name'],
                            "vehicle_number": row['Vehicle Number'],
                            "mobile": row['Mobile Number']
                        }
                }
        }

    elif row['Status'] == 'order_start_trip':
        order_data = {
            "status": "order_start_trip",
            "order_id": row['Order ID'],
            "order_details":
                {
                    "event_ts": row['Event Timestamp'],
                    "partner_location":
                        {
                            "lat": row['Latitude'],
                            "long": row['Longitude']
                        },
                    "estimated_trip_fare": row['Estimated Trip Fare']
                }
        }

    elif row['Status'] == 'order_end_job':
        order_data = {
            "status": "order_end_job",
            "order_id": row['Order ID'],
            "order_details":
                {
                    "event_ts": row['Event Timestamp'],
                    "actual_trip_fare": row['Actual Trip Fare']
                }
        }

    elif row['Status'] == 'order_reopen':
        order_data = {
                "status": "order_reopen",
                "order_id": row['Order ID'],
                "order_details":
                    {
                        "event_ts": row['Event Timestamp']
                    }
            }

    elif row['Status'] == 'Order Cancelled':
        order_data = {
            "status": "order_reopen",
            "order_id": row['Order ID'],
            "order_details":
                {
                    "event_ts": row['Event Timestamp']
                }
        }

    # Send the POST request
    send_order_update(order_data)

    # Wait for 5 seconds before sending the next request
    time.sleep(5)
