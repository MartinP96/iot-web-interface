from flask import Flask
from iot_web_interface import sql_client
import csv

if __name__ == '__main__':
    print('test')

    # Create MySQL client
    client = sql_client.MySqlClient()

    # Read SQL configuration
    with open("configuration/sql_configuration.csv") as f:
        reader = csv.DictReader(f)
        sql_configuration_dict = next(reader)

    # Connect to SQL
    ret = client.connect_sql(host=sql_configuration_dict["host"],
                             database=sql_configuration_dict["database"],
                             user=sql_configuration_dict["user"],
                             password=sql_configuration_dict["password"])

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello!'

    @app.route('/data')
    def get_data():
        data = {
            'data': '123',
            'timestamp': '10.05.2023'
        }
        return data

    @app.route('/device_list')
    def get_device_list():
        data = client.execute_stored_procedure("GetDeviceList")
        return data

    @app.route('/device_last_measurement')
    def get_last_measurements_for_device():
        data = client.execute_stored_procedure("GetLastMeasurementForDevice", (1,))
        return data

    app.run(host="192.168.0.101")
