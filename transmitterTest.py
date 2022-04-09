import digitalio
import board
import busio
import adafruit_rfm9x

CS = digitalio.DigitalInOut(board.D5) # Change this if we need to use a different pin because of the canBus
RESET = digitalio.DigitalInOut(board.D6) # - - - ^
spi = busio.SPI(board.D11, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0) # 10mhz is the standard baudrate (baudrate=1000000

# Should be as simple as using this command
rfm9x.send('TestExampleData1234567890'.encode()) # Maximum packet size is 60 BYTES.  So 60 characters maximum

# Should be as simple as using this command to recieve
#print(rfm9x.receive(timeout=5.0)) # this command will wait 5 seconds to try and recieve a packet before timing out.