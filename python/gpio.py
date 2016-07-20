import machine
import type

ch_on = [machine.Pin(0, machine.Pin.OUTPUT, machine.Pin.PULL_UP)]
ch_off = [machine.Pin(5, machine.Pin.OUTPUT, machine.Pin.PULL_UP)]

def switch(channel, value):
    if value == 1:
        pin = ch_on[channel]
    else:
        pin = ch_off[channel]
    pin.high()
    time.sleep(0.5)
    pin.low()
    
switch(0, 1)
time.sleep(10)
switch(0, 0)
