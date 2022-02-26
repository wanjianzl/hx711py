import time
import sys
from xml.sax.handler import property_interning_dict

EMULATE_HX711=True

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()

print("Ready!")

weight = hx.get_weight(5)
error = 5
while True:
    try:
        current_weight = hx.get_weight(5)
        print('current_weight:', current_weight)
        if current_weight - weight > error:
            print('Ding,Dong')
            weight = current_weight
        if weight - current_weight > error:
            print('Alarm!!!')
            weight = current_weight
            
        hx.power_down()
        hx.power_up()
        time.sleep(1) #1 second

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
