import machine

def received_button_press(pin):
  print("Button %d On Pressed!" % pin)

ch1_on = machine.Pin(12, machine.Pin.IN)
ch1_off = machine.Pin(14, machine.Pin.IN)

ch_on.irq(trigger=machine.Pin.IRQ_FALLING, handler=received_button_press)
ch_off.irq(trigger=machine.Pin.IRQ_FALLING, handler=received_button_press)
