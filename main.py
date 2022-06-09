from threading import Thread
import os
import json
import sqlite3
from unicodedata import name
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask_jsonpify import jsonify
#from find import my_dict
#from find import list


# db_connect = create_engine('sqlite:///chinook.db')

# def get_connection():
#    return sqlite3.connect("chinook.db")


APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, '/')


app = Flask(__name__, static_url_path='', static_folder='', template_folder='')
api = Api(app)


class DeviceDataProcessing(Resource):

    def post(self):
        """
        Method for receive data for db
        """
        data_obj = request.form
        clicked_device_name = data_obj.get('clicked_device_name')
        mac_device_address = data_obj.get('mac_device_address')
        operation_result = os.popen(f'sudo rfcomm connect hci0 {mac_device_address}')
        
        operation_result_text = operation_result.read()

        # если успешно подключено, то сообщения об ошибке не высвечивается
        if not operation_result_text:
           operation_result_text = f'Successfully connected. Device name: {clicked_device_name} with Mac={mac_device_address}'
           
        return jsonify({'operation_result_text': operation_result_text})
        

api.add_resource(DeviceDataProcessing, '/process_device_data')

class Device():
    def __init__(self, device_name, mac_address) -> None:
        self.device_name = device_name
        self.mac_address = mac_address

@app.route("/")
def hello_world():
    devices_for_user = []
    # Логика вычитывает девайсы в сети раз в 30 сек
    devices_in_network = [('jbl','04:CB:88:75:CA:47'), ('Windows', 777), ('Linux', 5431)]
    
    for item in devices_in_network:
        devices_for_user.append(Device(item[0], item[1]))

    return render_template("index.html", devices=devices_for_user)

if __name__ == '__main__':
     app.run(port='5040')
