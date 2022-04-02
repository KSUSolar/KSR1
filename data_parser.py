import can
from can_message import *

def recieve_message():
    bus = can.interface.Bus(interface='socketcan', channel='can1')
    parsed_message = []
    while True:
        message = bus.recv()
        if (message.arbitration_id == pack_id):
            parsed_message.append(message.data[pack_current])
            parsed_message.append(message.data[pack_inst_voltage])
            parsed_message.append(message.data[pack_SOC])
            parsed_message.append(message.data[relay_state])
            break
    while True:
        message = bus.recv()
        if (message.arbitration_id == temp_id):
            parsed_message.append(message.data[high_temp])
            parsed_message.append(message.data[low_temp])
            parsed_message.append(message.data[avg_temp])
            parsed_message.append(message.data[high_temp_id])
            parsed_message.append(message.data[low_temp_id])
            break
    while True:
        message = bus.recv()
        if (message.arbitration_id == cell_id):
            parsed_message.append(message.data[low_cell_voltage])
            parsed_message.append(message.data[high_cell_voltage])
            parsed_message.append(message.data[avg_cell_voltage])
            parsed_message.append(message.data[current_ADC1])
            parsed_message.append(message.data[current_ADC2])
            parsed_message.append(message.data[min_cell_voltage])
            parsed_message.append(message.data[max_cell_voltage])
            break   
    return parsed_message

if __name__ == '__main__':
    print(recieve_message())