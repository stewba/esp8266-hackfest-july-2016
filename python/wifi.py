import network
import time

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

ap_if.active(False)
sta_if.active(True)

while not sta_if.isconnected():
	sta_if.connect('ssid', 'password')
	time.sleep(5)

	print(sta_if.ifconfig())
