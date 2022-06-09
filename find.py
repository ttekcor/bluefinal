import os
from platform import mac_ver
import sqlite3

conn = sqlite3.connect("data1.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


def add_headset(name_device,mac_address):
    command = "INSERT INTO DEVICES (NAME_DEVICE,MAC_ADDRESS) VALUES('{}','{}');".format(name_device, mac_address)
    conn.execute(command)
    conn.commit()

class person:
    def __init__(self,mac,name):
        self.name = name
        self.mac = mac
devices_for_write_to_db_dict = {}
list0 = []
ui =True

while ui:
    operation_command = os.popen(f'hcitool scan')
    a = operation_command.read()[14:].split()
    p1 = person(a[0],a[1])
    devices_for_write_to_db_dict[p1.name] = p1.mac
    print (devices_for_write_to_db_dict)        
    list0.append(p1.name)
    all_devices_in_network_list = list(set(list0)) 
    print (all_devices_in_network_list)

    for device_name in all_devices_in_network_list:
        query_for_sql = "SELECT * FROM DEVICES WHERE NAME_DEVICE='{}'".format(device_name)
        command_result = conn.execute(query_for_sql)
        command_result =  command_result.fetchall()

        if command_result:
            devices_for_write_to_db_dict.pop(device_name)

    # добавляем только элементы которых не было ранее в таблице            
    for name_device,mac_address in devices_for_write_to_db_dict.items():
        add_headset(name_device,mac_address)