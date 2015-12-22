Raspberry Pi Audio Output component. Part of the [Crossbar.io IoT Cookbook](http://crossbar.io/iotcookbook/). For more information, including usage instructions, see the [component documentation](http://crossbar.io/iotcookbook/Raspberry-Pi-Audio-Output/).


For this we are using [pi-switch-python](https://github.com/lexruee/pi-switch-python).

The local Crossbar.io serves the control page and can route calls.

To run do

```
sudo python poweroutlet_pi.py
```

on the Pi.

Without additional arguments, this connects to "192.68.1.136:8080/ws" for realm "iot_cookbook".

```
   sudo python poweroutlet_pi.py --router 'ws://demo.crossbar.io:8080'  --realm  'realm1'
```

(sudo because the GPIO access lib requires it)

Pins to connect to the 433 Mhz sender on the Pi:

2 - 5v
6 - GND
11 - GPIO 17

