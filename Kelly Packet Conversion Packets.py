packet1 = [0, 0, 0, 0, 130, 4, 10, 64]
packet2 = [0, 80, 70, 0, 0, ]
#battery voltage, motor temp, controller temp, errors

#packet 1:
rpm = (packet1[1]*256) + packet1[0]
motorCurrent = ((packet1[3]*256) + packet1[2])/10
batteryVoltage = ((packet1[5]*256) + packet1[4])/10
print("RPM: " + str(rpm))
print("Motor Current: " + str(motorCurrent))
print("Battery Voltage: " + str(batteryVoltage))

#error code (lsb4 and msb10), range is 1-7, and then msb is 8-15
errorCode1 = str(bin(packet1[6]))[2:]
errorCode2 = str(bin(packet1[7]))[2:] #[2:] removes first and second character (the added 0b when converting to binary)

#a way to add the zeros in fron that might not be there from converting, and we need an 8 bit, so this adds 0s in front
if len(errorCode1) < 8:
    i = len(errorCode1)%8
    while i < 8:
        errorCode1 = "0" + errorCode1
        i+=1

if len(errorCode2) < 8:
    i = len(errorCode2)%8
    while i < 8:
        errorCode2 = "0" + errorCode2
        i+=1

#This loop will search for which 1s exist in the binary error code and print which error number it is
x = 8
for i in errorCode1:
    x -= 1
    if (i == "1"):
        print("ERR " + str(x))
#print(errorCode1) #for testing purposes

x = 16
for i in errorCode2:
    x -= 1
    if (i == "1"):
        print("ERR " + str(x))
#print(errorCode2) #for testing purposes

###################################################################################################################################################
#message 2:

#Throttle:
print("Throttle Signal: " + str((packet2[0]*5)/255) + "V") #converts number from something/255 to something/5 because its out of 5V

#Temperature:
print("Controller Temperature: " + str(packet2[1]) + "C")
print("Temperature: " + str(packet2[1]-40) + "C") #is the array giving us the controller temp or the actual temp? (I assumed controller temp)
print("Motor Temperature: " + str(packet2[2]-30) + "C")

message1 = str(bin(packet2[3]))[2:]
message2 = str(bin(packet2[4]))[2:]


#I have to make sure I have at least 4 digits at the end of the binary string for the next code to work:
if len(message1) < 4:
    i = len(message1)%4
    while i < 4:
        message1 = "0" + message1
        i+=1

#same thing but 8
if len(message2) < 8:
    i = len(message2)%8
    while i < 8:
        message2 = "0" + message2
        i+=1

message1last = str(int(message1[len(message1)-2:len(message1)], 2)) #have to convert the two digits to decimal for the 4 output options (0-3)
print("Status of Command: " + message1last) 

message1beginning = str(int(message1[len(message1)-4:len(message1)-2], 2))
print("Status of Feedback: " + message1beginning)


#this might be able to be made more efficient, or into a function if needed in other areas
if (int(message2) > 0):
    print("Status of Switch Signals: ", end = "")
    if (message2[len(message2)-8:len(message2)-7] == "1"):
        print("Boost Switch, ", end = "")
    if (message2[len(message2)-7:len(message2)-6] == "1"):
        print("Foot Switch, ", end = "")
    if (message2[len(message2)-6:len(message2)-5] == "1"):
        print("Forward Switch, ", end = "")
    if (message2[len(message2)-5:len(message2)-4] == "1"):
        print("Backward Switch, ", end = "")
    if (message2[len(message2)-4:len(message2)-3] == "1"):
        print("12V Brake Switch, ", end = "")
    if (message2[len(message2)-3:len(message2)-2] == "1"):
        print("Hall C, ", end = "")
    if (message2[len(message2)-2:len(message2)-1] == "1"):
        print("Hall B, ", end = "")
    if (message2[len(message2)-1:len(message2)] == "1"):
        print("Hall A, ", end = "")
    print("")


