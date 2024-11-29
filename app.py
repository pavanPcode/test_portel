import mysql.connector
from flask import Flask, request

# Flask application setup
app = Flask(__name__)

# MySQL connection setup
db_config = {
    'host': 'MYSQL5048.site4now.net',
    'user': 'a50d85_payroll',  # Replace with your MySQL username
    'password': 'p3r3nnial',  # Replace with your MySQL password
    'database': 'db_a50d85_payroll'  # Replace with your database name
}
#
def insert_order_update(order_data):
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Prepare SQL query using .format() for string formatting
    query = """
    INSERT INTO Porter_order_updates 
    (order_id, status, event_ts, lat, `long`, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare, reopen_event_ts)
    VALUES ('{order_id}', '{status}', {event_ts}, {lat}, {long}, '{driver_name}', '{vehicle_number}', '{mobile}', {estimated_trip_fare}, {actual_trip_fare}, {reopen_event_ts})
    """.format(
        order_id=order_data['orderId'],
        status=order_data['status'],
        event_ts=order_data['orderDetails'].get('eventTs', 'NULL'),
        lat=order_data['orderDetails'].get('partnerLocation', {}).get('lat', 'NULL'),
        long=order_data['orderDetails'].get('partnerLocation', {}).get('long', 'NULL'),
        driver_name=order_data['orderDetails'].get('driverDetails', {}).get('driverName', 'NULL'),
        vehicle_number=order_data['orderDetails'].get('driverDetails', {}).get('vehicleNumber', 'NULL'),
        mobile=order_data['orderDetails'].get('driverDetails', {}).get('mobile', 'NULL'),
        estimated_trip_fare=order_data['orderDetails'].get('estimatedTripFare', 'NULL'),
        actual_trip_fare=order_data['orderDetails'].get('actualTripFare', 'NULL'),
        reopen_event_ts=order_data['orderDetails'].get('eventTs', 'NULL')
    )
    print(query)
    # Execute the query
    cursor.execute(query)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

# Function to insert order update into the database
# def insert_order_update(order_data):
#     # Connect to MySQL
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#
#     # Prepare SQL query
#     query = """
#     INSERT INTO Porter_order_updates
#     (order_id, status, event_ts, lat, long, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare, reopen_event_ts)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#
#     # Extract order details from the webhook payload
#     order_id = order_data['orderId']
#     status = order_data['status']
#     event_ts = None
#     lat = long = driver_name = vehicle_number = mobile = estimated_trip_fare = actual_trip_fare = reopen_event_ts = ''
#
#     if status == "order_accepted":
#         event_ts = order_data['orderDetails']['eventTs']
#         lat = order_data['orderDetails']['partnerLocation']['lat']
#         long = order_data['orderDetails']['partnerLocation']['long']
#         driver_name = order_data['orderDetails']['driverDetails']['driverName']
#         vehicle_number = order_data['orderDetails']['driverDetails']['vehicleNumber']
#         mobile = order_data['orderDetails']['driverDetails']['mobile']
#
#     elif status == "order_start_trip":
#         lat = order_data['orderDetails']['partnerLocation']['lat']
#         long = order_data['orderDetails']['partnerLocation']['long']
#         estimated_trip_fare = order_data['orderDetails']['estimatedTripFare']
#
#     elif status == "order_end_job":
#         event_ts = order_data['orderDetails']['eventTs']
#         actual_trip_fare = order_data['orderDetails']['actualTripFare']
#
#     elif status == "order_cancel":
#         event_ts = order_data['orderDetails']['eventTs']
#
#     elif status == "order_reopen":
#         reopen_event_ts = order_data['orderDetails']['eventTs']
#
#     # Execute the query
#     cursor.execute(query, (
#     order_id, status, event_ts, lat, long, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare,
#     reopen_event_ts))
#     conn.commit()
#
#     # Close the connection
#     cursor.close()
#     conn.close()


# Define the route to receive webhooks
@app.route('/porter/order_update', methods=['POST'])
def order_update():
    try:
        # Get the JSON data from the webhook
        webhook_data = request.json

        # Check status and insert data based on status type
        if webhook_data['status'] == 'order_accepted':
            insert_order_update(webhook_data)
        elif webhook_data['status'] == 'order_start_trip':
            insert_order_update(webhook_data)
        elif webhook_data['status'] == 'order_end_job':
            insert_order_update(webhook_data)
        elif webhook_data['status'] == 'order_cancel':
            insert_order_update(webhook_data)
        elif webhook_data['status'] == 'order_reopen':
            insert_order_update(webhook_data)

        # Respond with a success message
        return 'Webhook received and saved to database', 200
    except Exception as e:
        # If an error occurs, respond with an error message
        print(f"Error: {e}")
        return 'Failed to process webhook', 500

#
if __name__ == '__main__':
    app.run()
