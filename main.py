from flask import Flask


if __name__ == '__main__':
    print('test')
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

    app.run(host="192.168.0.101")

