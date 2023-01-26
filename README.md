# KSR1
Data Logging, Dashboard, and Wireless Communication for the KSR 

# canBus Hat Setup
In the very bottom of the /boot/config.txt file put:
dtoverlay=spi1-2cs
dtoverlay=mcp2515-can0, oscillator8000000, interrupt=25, spimaxfrequency=1000000

spi1-2cs = creates the spi1 interface with 2 chip selects
mcp2515-can0 = sets up the canhat with the correct library at a network interface.
You can check it worked by using "ifconfig can0" in the terminal