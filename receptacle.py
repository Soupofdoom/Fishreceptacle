import datetime
import time
import random
import outputgpio
import threading
from math import ceil
#Settings
beginsunup = 8
sunup = 9
stormstart = 20 #Start of storm (24H)
stormstop = 21 #End of strom (24H)
resetday = 6 #Day of randomisation, Sunday = 0

#Define GPIO pins for RGB
#Pair1
R1 = 2
G1 = 3
B1 = 4
#Pair2
R2 = 27
G2 = 10
B2 = 9
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
#Spares
#24
#25
#8
#7
#12
#16
#20
#21
#17

#define vars
level = 0
targetlevel = 0
whatday = 0
hasrandomed = False
levelstep = 1
#Define Functions
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
        outputgpio.set_value(128)
        time.sleep(5)
        outputgpio.set_value(0)
        print("Test Complete")

def sunrise():
            print("Sunup")
            redaim = 50
            redlevel = 0
            greenaim = 50
            greenlevel = 0
            blueaim = 50
            bluelevel = 0
            threading.start_new_thread(outputgpio.fadein(redaim,  redlevel))
            #thread.start_new_thread(outputgpio.fadein(greenaim,  greenlevel))
            #thread.start_new_thread(outputgpio.fadein(blueaim,  bluelevel))
            time.sleep(60)
            
def RGBPercentages(RGBPercent):
        RGBPercent = int(ceil(128/100*RGBPercent))
        print('Percentage output level:', RGBPercent)
        return RGBPercent
#Program loop ---------------------------------------------------------------------------------------------------------
while 1 != 2:    
    today =int(datetime.date.today().strftime("%w"))
    now = int(datetime.datetime.now().strftime("%H"))
    #RGBPercentages(int(input('%?'))) #Debugging Line
    while 1 == 1: #beginsunup <= now < sunup:
        sunrise()
    if today == resetday and hasrandomed == False: 
        whatday = randomday()
        hasrandomed = True
    
    while today == whatday and stormstart <= now < stormstop:
            print('Make it rain!')
            break
    
    print('Today:', today)
    print('whatday:', whatday)
    targetlevel = int(input('Where to?'))
    
    if targetlevel != level: 
        if targetlevel > 128 or targetlevel < 0:
            print('Level too high/low, lamptest instead!')
            lamptest() 
        elif targetlevel < level:
            #if levelstep <=0:
                #levelstep = levelstep *-1
            outputgpio.fadeout(targetlevel, level)
        elif targetlevel > level:
            #if levelstep >= 0:
                #levelstep = levelstep * -1
            outputgpio.fadein(targetlevel,  level)
        level = targetlevel

    print('end')