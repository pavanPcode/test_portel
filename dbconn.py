import mysql.connector

# MySQL connection setup
db_config = {'host': 'MYSQL5048.site4now.net',
             'user': 'a50d85_payroll',
             'password': 'p3r3nnial',
             'database': 'db_a50d85_payroll'  }

def store_order_details(order_data):
    insert_query = """
    INSERT INTO Porter_CreatedOrders (request_id, order_id, estimated_pickup_time, currency, minor_amount, tracking_url)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
    INSERT INTO Porter_OrderLog (order_id, order_type)
    VALUES ('{1}', 'Created')
    """.format(order_data.get('request_id'),order_data.get('order_id'),order_data.get('estimated_pickup_time'),
               order_data['estimated_fare_details']['currency'],order_data['estimated_fare_details']['minor_amount'],
               order_data.get('tracking_url'))
    print(insert_query)
    try:
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # # Extract data
        # request_id = order_data.get('request_id')
        # order_id = order_data.get('order_id')
        # estimated_pickup_time = order_data.get('estimated_pickup_time')
        # currency = order_data['estimated_fare_details']['currency']
        # minor_amount = order_data['estimated_fare_details']['minor_amount']
        # tracking_url = order_data.get('tracking_url')

        # Execute insert query
        cursor.execute(insert_query)
        db.commit()
        print("Order details successfully stored.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def fetch_record(query):
    try:
        # Establish database connection
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        # Execute query
        cursor.execute(query)
        result = cursor.fetchone()

        # Check if result is empty or not
        if result:
            return {"status": True, "result": result}
        else:
            return {"status": False, "result": 'no data found'}
    except mysql.connector.Error as e:
        return {"status": False, "error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def insert_order_update(order_data,order_type):
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Prepare SQL query using .format() for string formatting
    query = """
    INSERT INTO Porter_order_updates 
    (order_id, status, event_ts, lat, `long`, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare, reopen_event_ts)
    VALUES ('{order_id}', '{status}', {event_ts}, {lat}, {long}, '{driver_name}', '{vehicle_number}', '{mobile}', {estimated_trip_fare}, {actual_trip_fare}, {reopen_event_ts});
    INSERT INTO Porter_OrderLog (order_id, status)
    VALUES ('{order_id}', '{order_type}')
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
        reopen_event_ts=order_data['orderDetails'].get('eventTs', 'NULL'),
        order_type = order_type
    )
    print(query)
    # Execute the query
    cursor.execute(query)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()