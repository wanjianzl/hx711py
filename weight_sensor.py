import time
import sys
 
from pygame import mixer
from hx711 import HX711
import RPi.GPIO as GPIO
    
LedPin = 17 # LED light GIPO Number
 
# Initialize weight sensor, speaker mixer and LED light
def initialize():
    GPIO.setmode(GPIO.BCM) # Use GPIO number mode
    GPIO.setwarnings(False) # Disable GPIO warning
    GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH) # This makes the LED light off
 
    mixer.init() # initialize speaker mixer
 
    hx = HX711(24, 18) # Config weight sensor GPIO numbers
    hx.set_reading_format("MSB", "MSB") # Config how sensor read the signal
 
    # How to calculate the reference unit to calibrate the weight sensor.
    # To set the reference unit, put 1000 grams on your sensor or 
    # anything you have and know exactly how much it weights.
    # I got numbers around -2600 when I put 1000 grams. So, according to the rule:
    # If 1000 grams is -2600 then 1 grams is -2600 / 1000 = -2.6.
    # So reference unit is 2.6
    referenceUnit = -2.6
    hx.set_reference_unit(referenceUnit)
 
    # Initialize the weight sensor
    hx.reset()
    hx.tare()
 
    print("Ready!")
    return hx
 
# Clean up GPIO, speaker mixer, LED light and exit application
def cleanAndExit():
    print("Cleaning...")
    mixer.music.stop()
    GPIO.output(LedPin, GPIO.HIGH) # light off
    GPIO.cleanup()
    print("Bye!")
    sys.exit()
 
# Play dingdong sound
def playDingdong():
    mixer.music.load('/home/pi/hx711py/dingdong.mp3')
    mixer.music.set_volume(1.0)
    mixer.music.play()
    
# Play alarm sound
def playAlarm():
    mixer.music.load('/home/pi/hx711py/burglar-alarm-sound.mp3')
    mixer.music.set_volume(1.0)
    mixer.music.play()
    lightOn()
 
# Blink LED light 10 times in case of alarming
def lightOn():
    for i in range(10): # loop 10 times
        GPIO.output(LedPin, GPIO.LOW) # light on
        time.sleep(0.2) # sleep 0.2 second
        GPIO.output(LedPin, GPIO.HIGH) # light off
        time.sleep(0.2) # sleep 0.2 second
 
hx = initialize() # Initialize weight sensor, speaker mixer and LED light then return weight sensor
weight = hx.get_weight(5) # Get weight by average 5 times
error = 50 # Tolerance for weight sensor, because weight sensor is not accurate
while True:
    try:
        current_weight = hx.get_weight(5) # Get current weight by average 5 times
        print('current_weight:', current_weight)
        if current_weight - weight > error: # If someone put the package on the mat
            print('Ding,Dong!!!')
            playDingdong()
            weight = current_weight
        elif weight - current_weight > error: # Else if someone steal the package from the mat
            print('Alarm!!!')
            playAlarm()
            weight = current_weight
            
        time.sleep(1) # Wait 1 second then loop again
 
    finally:
        cleanAndExit() # in case of any error, do the clean up and exit
        
