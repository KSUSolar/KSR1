import can

### This is for testing from a file ###
# from can_message import *

def recieve_message():
    
    bus = can.interface.Bus(interface='socketcan', channel='can0', baudrate=500000)
    parsed_message = []
    
    while True:
        message = bus.recv()
        if (message.arbitration_id == 1712): # replace with pack_id if using file
            # print(message)
            parsed_message.append(message.data[1]) # Current
            parsed_message.append(message.data[3]) # Voltage
            parsed_message.append(message.data[5]) # pack_SOC
            # print(parsed_message)
            break
    while True:
        message = bus.recv()
        if (message.arbitration_id == 1713):
            # print(message)
            parsed_message.append(message.data[0]) # high_temp
            parsed_message.append(message.data[1]) # low_temp
            parsed_message.append(message.data[2]) # avg_temp
            parsed_message.append(message.data[3]) # high_temp_id
            parsed_message.append(message.data[4]) # low_temp_id
            #print(parsed_message)
            break
    return parsed_message

if __name__ == '__main__':
    print(recieve_message())