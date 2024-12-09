import mysql.connector
from datetime import datetime
import pytz

# MySQL connection setup
db_config = {'host': 'MYSQL5048.site4now.net',
             'user': 'a50d85_payroll',
             'password': 'p3r3nnial',
             'database': 'db_a50d85_payroll'  }


def db_createorder(order_data,request_id):
        try:
            # Prepare the SQL query
            insert_query = """
            INSERT INTO Porter_delivery_Address (
                request_id, instructions_text, 
                pickup_apartment_address, pickup_street_address1, pickup_street_address2, pickup_landmark, 
                pickup_city, pickup_state, pickup_pincode, pickup_country, pickup_lat, pickup_lng, 
                pickup_contact_name, pickup_contact_phone, 
                drop_apartment_address, drop_street_address1, drop_street_address2, drop_landmark, 
                drop_city, drop_state, drop_pincode, drop_country, drop_lat, drop_lng, 
                drop_contact_name, drop_contact_phone, additional_comments
            ) VALUES (
                '{0}', '{1}',
                '{2}', '{3}', '{4}', '{5}', 
                '{6}', '{7}', '{8}', '{9}', {10}, {11},
                '{12}', '{13}', 
                '{14}', '{15}', '{16}', '{17}',
                '{18}', '{19}', '{20}', '{21}', {22}, {23},
                '{24}', '{25}', '{26}'
            );
            """.format(
                request_id,
                order_data['delivery_instructions']['instructions_list'][0]['description'],
                order_data['pickup_details']['address']['apartment_address'],
                order_data['pickup_details']['address']['street_address1'],
                order_data['pickup_details']['address']['street_address2'],
                order_data['pickup_details']['address']['landmark'],
                order_data['pickup_details']['address']['city'],
                order_data['pickup_details']['address']['state'],
                order_data['pickup_details']['address']['pincode'],
                order_data['pickup_details']['address']['country'],
                order_data['pickup_details']['address']['lat'],
                order_data['pickup_details']['address']['lng'],
                order_data['pickup_details']['address']['contact_details']['name'],
                order_data['pickup_details']['address']['contact_details']['phone_number'],
                order_data['drop_details']['address']['apartment_address'],
                order_data['drop_details']['address']['street_address1'],
                order_data['drop_details']['address']['street_address2'],
                order_data['drop_details']['address']['landmark'],
                order_data['drop_details']['address']['city'],
                order_data['drop_details']['address']['state'],
                order_data['drop_details']['address']['pincode'],
                order_data['drop_details']['address']['country'],
                order_data['drop_details']['address']['lat'],
                order_data['drop_details']['address']['lng'],
                order_data['drop_details']['address']['contact_details']['name'],
                order_data['drop_details']['address']['contact_details']['phone_number'],
                order_data['additional_comments']
            )

            # Connect to the database
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            # Execute the query
            cursor.execute(insert_query)
            db.commit()

            return {'status':True,"message": "Order details successfully inserted", "request_id": request_id}

        except mysql.connector.Error as e:
            return {"error": str(e),'status':False}
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()


def store_order_details(order_data):
    # SQL queries
    insert_query_orders = """
    INSERT INTO Porter_CreatedOrders (request_id, order_id, estimated_pickup_time, currency, minor_amount, tracking_url)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    insert_query_logs = """
    INSERT INTO Porter_OrderLog (order_id, order_type)
    VALUES (%s, %s);
    """

    try:
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Data for the queries
        order_data_values = (
            order_data.get('request_id'),
            order_data.get('order_id'),
            order_data.get('estimated_pickup_time'),
            order_data['estimated_fare_details']['currency'],
            order_data['estimated_fare_details']['minor_amount'],
            order_data.get('tracking_url')
        )
        order_log_values = (
            order_data.get('order_id'),
            'order_Created'
        )

        # Execute insert queries
        cursor.execute(insert_query_orders, order_data_values)
        cursor.execute(insert_query_logs, order_log_values)
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


def insert_webhook_payload(payload):
    try:
        # Get current IST time
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Common values
        order_id = payload['order_id']
        status = payload['status']
        order_details = payload['order_details']
        event_ts = order_details.get('event_ts', None)

        # Prepare SQL queries
        query_order_update = """
        INSERT INTO Porter_order_updates 
        (order_id, status, event_ts, lat, `long`, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare, reopen_event_ts)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        query_order_log = """
        INSERT INTO Porter_OrderLog (order_id, order_type, created_on)
        VALUES (%s, %s, %s);
        """

        # Extract fields based on type
        lat, long, driver_name, vehicle_number, mobile = None, None, None, None, None
        estimated_trip_fare, actual_trip_fare = None, None

        if 'partner_location' in order_details:
            lat = order_details['partner_location'].get('lat', None)
            long = order_details['partner_location'].get('long', None)

        if 'driver_details' in order_details:
            driver_details = order_details['driver_details']
            driver_name = driver_details.get('driver_name', None)
            vehicle_number = driver_details.get('vehicle_number', None)
            mobile = driver_details.get('mobile', None)

        if 'estimated_trip_fare' in order_details:
            estimated_trip_fare = order_details['estimated_trip_fare']

        if 'actual_trip_fare' in order_details:
            actual_trip_fare = order_details['actual_trip_fare']

        # Insert values
        order_update_values = (
            order_id, status, event_ts, lat, long,
            driver_name, vehicle_number, mobile,
            estimated_trip_fare, actual_trip_fare, event_ts
        )

        order_log_values = (order_id, status, current_time)

        # Execute queries
        cursor.execute(query_order_update, order_update_values)
        cursor.execute(query_order_log, order_log_values)

        # Commit transaction
        conn.commit()

        print("Webhook payload inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        cursor.close()
        conn.close()
