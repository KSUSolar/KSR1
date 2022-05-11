# KSR1
Data Logging, Dashboard, and Wireless Communication for the KSR 


# Just in case you need to setup the canBus hat again or the autostart
# Autostart #
The autostart .desktop file is located here:
/etc/xdg/autostart/display.desktop
with this in the file:
[Desktop Entry]
Name={Whatever you want}
Exec=/usr/bin/python {whatever .py file you want to run}

# canBus Hat Setup #
In the very bottom of the /boot/config.txt file put:
dtoverlay=spi1-2cs
dtoverlay=mcp2515-can0, oscillator8000000, interrupt=25, spimaxfrequency=1000000

spi1-2cs = creates the spi1 interface with 2 chip selects
mcp2515-can0 = sets up the canhat with the correct library at a network interface.
You can check it worked by using "ifconfig can0" in the terminal