import datetime
import time
import random
import threading
from math import ceil
import RPi.GPIO as GPIO

#Settings
beginsunup = 8
sunup = 9
stormstart = 20 #Start of storm (24H)
stormstop = 21 #End of strom (24H)
resetday = 0 #Day of randomisation, Sunday = 0
fadedelay = 0

#Define GPIO pins for RGB
LEDCount = 3
SPI_CS_PIN = 17
SPI_CLK_PIN = 23
SPI_SDISDO_PIN = 22 # mosi

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_SDISDO_PIN, GPIO.OUT)

#Pair1
R1 = 2
#GPIO.setup(R1, GPIO.OUT)
G1 = 3
#GPIO.setup(G1, GPIO.OUT)
B1 = 4
#GPIO.setup(B1, GPIO.OUT)

#Pair2
R2 = 27
#GPIO.setup(R2, GPIO.OUT)
G2 = 10
#GPIO.setup(G1, GPIO.OUT)
B2 = 9
#GPIO.setup(B1, GPIO.OUT)
#Pair3
R3 = 11
G3 = 5
B3 = 6
#Pair4
R4 = 13
G4 = 19
B4 = 26
#Pair5
R5 =14
G5 = 15
B5 = 18
#-------Spares
#24
#25
#8
#7
#12
#16
#20
#21
#17

#define vars + Setup
redlevel = 0
redtargetlevel = 0
greenlevel = 0
greentargetlevel = 0
bluelevel = 0
bluetargetlevel = 0
whatday = 0
hasrandomed = False
levelstep = 1
today = 0
now = 0
red = 0
green = 0
blue = 0
HEX_value = '#000000'

#Define Functions
def set_value(value):
    '''LEDCount = 3
    for i in range(1, (LEDCount + 1)):
        print('LEDCount:', i)
        threadcheck = threading.currentThread().getName()
        print(threadcheck)
        if threadcheck == 'RedThread':
            print('Woo')
        elif threadcheck == 'BlueThread':
            print('Blue')
        elif threadcheck == 'GreenThread':
            print('Green')'''
        #print ("Chip Select True")
    GPIO.output(SPI_CS_PIN, True)
        #print("Clock Pin False")
    GPIO.output(SPI_CLK_PIN, False)
        #print("Chip select False")
    GPIO.output(SPI_CS_PIN, False)

    b = '{0:016b}'.format(value)
    for x in range(0, 16):
            #output to pins, prints for testing
            #print(int(b[x]))
            GPIO.output(SPI_SDISDO_PIN, int(b[x]))
            #print("Clock Pin True")
            GPIO.output(SPI_CLK_PIN, True)
            #print("Clock Pin False")
            GPIO.output(SPI_CLK_PIN, False)
    
        #print ("Chip Select True")
    GPIO.output(SPI_CS_PIN, True)

def randomday():
        x = random.randint(1, 7)
        #if x == 1:
           #x = 'Monday'
        #elif x==2:
           #x = 'Tuesday'
        #elif x==3:
           #x  = 'Wednesday'
        #elif x==4:
           #x  = 'Thursday'
        #elif x==5:
           #x  = 'Friday'
        #elif x==6:
           #x  = 'Saturday'
        #elif x==7:
           #x  ='Sunday'
        #else:
           #print('Error')
        return x
        
def lamptest():
        print("Lamptest")
        #GPIO.output(R1, True)
        #GPIO.output(R2,True)
        #GPIO.output(R3,True)
        #GPIO.output(R4, True)
        #GPIO.output (R5, True)
        #GPIO.output(G1, True)
        #GPIO.output(G2,True)
        #GPIO.output(G3,True)
        #GPIO.output(G4, True)
        #GPIO.output (G5, True)
        #GPIO.output(B1, True)
        #GPIO.output(B2,True)
        #GPIO.output(B3,True)
        #GPIO.output(B4, True)
        #GPIO.output (B5, True)
        #GPIO.output(R1, True)
        #GPIO.output(R2,True)
        #GPIO.output(R3,True)
        #GPIO.output(R4, True)
        #GPIO.output (R5, True)
        set_value(128)
        time.sleep(5)
        set_value(0)
        print("Test Complete")

def fadein(targetlevel,  level):
    for level in range(level, targetlevel, 1):
        print ('level:' + str(level))
        set_value(level)
        time.sleep(fadedelay)
    
        
def fadeout(targetlevel,  level):
    for level in range(level, targetlevel,  -1):
        print ('level:' + str(level))
        set_value(level)
        time.sleep(fadedelay)
    level = targetlevel   
         
def decideinorout(targetlevel, level):
    if targetlevel != level:
        if targetlevel > 129 or targetlevel < -1:
            print('Level too high/low, lamptest instead!')
            lamptest() 
        elif targetlevel < level:
            #if levelstep <=0:
                #levelstep = levelstep *-1
            fadeout(targetlevel, level)
        elif targetlevel > level:
            #if levelstep >= 0:
                #levelstep = levelstep * -1
            fadein(targetlevel,  level)
            
     
    
    
def hex_to_rgb(HEX_value):
    HEX_value = HEX_value.lstrip('#')
    lv = len(HEX_value)
    return tuple(int(HEX_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
def RGB_to_pot(red,  green,  blue):
        print(red,  green,  blue,  'Func start')
        red = red/255*100
        green = green/255*100
        blue = blue/255*100
        red = int(ceil(128/100*red))
        green = int(ceil(128/100*green))
        blue = int(ceil(128/100*blue))
        print('Pot output level:', red, green, blue)
        return red,  green,  blue
        
def timeparameters():
    today =int(datetime.date.today().strftime("%w"))
    now = int(datetime.datetime.now().strftime("%H"))
    return today, now

#Program loop ---------------------------------------------------------------------------------------------------------
while 1 != 2:    
    today,  now = timeparameters()
    print('Pre R:', redtargetlevel, redlevel,  'G:', greentargetlevel, greenlevel, 'B:',  bluetargetlevel, bluelevel)
    HEX_value=str(input('Where to?'))
    #change HEX to RGB
    red,  green,  blue = hex_to_rgb(HEX_value)
    red ,  green,  blue = RGB_to_pot(red,  green,  blue)
    redtargetlevel = int(red)
    greentargetlevel = int(green)
    bluetargetlevel = int(blue)
    #threads for changing levels by fading
    Redthread = threading.Thread(name='RedThread', target=decideinorout(redtargetlevel, redlevel))
    Greenthread = threading.Thread(name='GreenThread', target=decideinorout(greentargetlevel, greenlevel))
    Bluethread = threading.Thread(name='BlueThread', target=decideinorout(bluetargetlevel, bluelevel))
    Redthread.start(); Bluethread.start(); Greenthread.start()
    threadcheck = threading.currentThread().getName()
    print(threadcheck)
    Redthread.join(); Bluethread.join(); Greenthread.join()
    redlevel = redtargetlevel
    greenlevel = greentargetlevel
    bluelevel = bluetargetlevel
    print('post R:', redtargetlevel, redlevel,  'G:', greentargetlevel, greenlevel, 'B:',  bluetargetlevel, bluelevel)
        #print(red,  green,  blue)
    while 1 == 1: #beginsunup <= now < sunup:
        break
    if today == resetday and hasrandomed == False: 
        whatday = randomday()
        hasrandomed = True
    
    while today == whatday and stormstart == now < stormstop:
            print('Make it rain!')
            break
    
    #print('Today:', today)
    #print('whatday:', whatday)
    #print('Now:', now)
    
    ''''if targetlevel != level: 
        if targetlevel > 129 or targetlevel < -1:
            print('Level too high/low, lamptest instead!')
            lamptest() 
        elif targetlevel < level:
            #if levelstep <=0:
                #levelstep = levelstep *-1
            outputgpio.fadeout(targetlevel, level)
            print(level)
        elif targetlevel > level:
            #if levelstep >= 0:
                #levelstep = levelstep * -1
            outputgpio.fadein(targetlevel,  level)
        level = targetlevel
    print(level)
'''
print('end')
