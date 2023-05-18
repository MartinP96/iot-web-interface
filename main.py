from flask import Flask, request
from flask import jsonify
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
        data = client.execute_stored_procedure("GetDeviceList", return_dict=False)

        data_dict = {}
        for dev_tuple in data:
            dev_dict = {
                "device_id": dev_tuple[0],
                "iot_configuration": dev_tuple[2]
            }
            data_dict[dev_tuple[1]] = dev_dict
        resp = jsonify(data_dict)
        return resp

    @app.route('/device_last_measurement/<dev_id>')
    def get_last_measurements_for_device(dev_id):
        data = client.execute_stored_procedure("GetLastMeasurementForDevice", (int(dev_id),), return_dict=False)
        measurements_dict = {}
        for data_tuple in data:
            measurement = {
                "measurement_id": data_tuple[0],
                "value": data_tuple[3],
                "measurement_unit": data_tuple[4],
                "insert_timestamp": data_tuple[5]
            }
            measurements_dict[data_tuple[2]] = measurement

        resp = jsonify(measurements_dict)
        return resp

    @app.route('/device_measurements_interval/')
    def device_measurements_interval():
        args = request.args
        data = client.execute_stored_procedure("GetMeasurementsOnInterval", (int(args['dev_id']),
                                                                             int(args['measurement_type']),
                                                                             args['interval_min'],
                                                                             args['interval_max']), return_dict=True)
        resp = jsonify(data)
        return resp

    # TMP Test POST
    # args = request.args

    app.run(host="192.168.0.101")

