import time
#import RPi.GPIO as GPIO

SPI_CS_PIN = 17
SPI_CLK_PIN = 23
SPI_SDISDO_PIN = 22 # mosi

#level = 0

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SPI_CS_PIN, GPIO.OUT)
#GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
#GPIO.setup(SPI_SDISDO_PIN, GPIO.OUT)

def set_value(value):
    #print ("Chip Select True")
    #GPIO.output(SPI_CS_PIN, True)
    #print("Clock Pin False")
    #GPIO.output(SPI_CLK_PIN, False)
    #print("Chip select False")
    #GPIO.output(SPI_CS_PIN, False)

    b = '{0:016b}'.format(value)
    for x in range(0, 16):
       #output to pins, prints for testing
        print(int(b[x]))
        #GPIO.output(SPI_SDISDO_PIN, int(b[x]))
        #print("Clock Pin True")
        #GPIO.output(SPI_CLK_PIN, True)
        #print("Clock Pin False")
        #GPIO.output(SPI_CLK_PIN, False)
    
    #print ("Chip Select True")
    #GPIO.output(SPI_CS_PIN, True)

def fadein(targetlevel,  level):
    for level in range(level, targetlevel, 1):
        print ('level:' + str(level))
        set_value(level)
        time.sleep(0.1)
    level = targetlevel
        
def fadeout(targetlevel,  level):
    for level in range(level, targetlevel,  -1):
        print ('level:' + str(level))
        set_value(level)
        time.sleep(0.1)
