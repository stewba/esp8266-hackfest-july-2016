import network
import time

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

ap_if.active(True)
sta_if.active(False)

ap_if.config(essid="FreeStuff",authmode=0)

while True:
  if not sta_if.isconnected():
    time.sleep(5)
  else:
    print(sta_if.ifconfig())