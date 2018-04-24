import time
import datetime
import random
import threading
#import importlib
from menu import *
import RPi.GPIO as GPIO
from neopixel import *
    #Welcome to hell.....
try:
    exitflag = False
    errorflag = False
    #------------------------------------file handling start
    
    #-------------------------------- file handling finish / variables begin
    today = 0
    now = 0
    
    upstart = 0
    upfinish = 0
    setstart = 0
    setfinish = 0
    stormtime = 0
    storms = 0
    stormlength = 0
    completestring = 0

    selection = 'F'
    #-------------------------------- variables end / Misc setup begins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(19, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(21, GPIO.IN)

    GPIO.output(25, GPIO.HIGH)
    
    # LED strip configuration:
    LED_COUNT      = 13      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0
    LED_STRIP      = ws.SK6812_STRIP_RGBW
    #LED_STRIP      = ws.SK6812W_STRIP
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    for i in range(strip.numPixels()):
                    strip.setPixelColor(i, 0)
                    strip.show()
                    time.sleep(0.1)
    time.sleep(3)

    #-------------------------------- Misc setup complete / Functions start
    def mainmenu():
        global selection
        global upstart
        global upfinish
        global setstart
        global setfinish
        global stormtime
        global storms
        global stormlength
        global completestring
        while selection != '0':  
            print('''Main Menu:
                1. Timer Settings
                2. Storm Settings
                3. Timer output
                0 - Shutdown''')
            selection = str(input('Where to?: '))
            if selection == '1':
                while selection != '0':
                    print('Settings Menu:')
                    print('1. Sunrise Start: ',upstart)
                    print('2. Sunrise Finish: ', upfinish)
                    print('3. Sunset Start: ', setstart)
                    print('4. Sunset Finish: ', setfinish)
                    print('H - Help')
                    print('0 - Backup')
                    selection = 'F'
                    selection = str(input('Where to? '))
            
                    if selection == '1':
                        print('Sunrise start: ', upstart)
                        update = str(input('New value? (24H):'))
                        if update != upstart:
                            if 0 < int(update) <= 2359:
                                if update < upfinish:
                                    if len(update) == 4:
                                        settingsupdate(update, upstart, completestring)
                                        upstart = update
                                    else:
                                        print('ERROR:Invalid value')
                                        errorflash()
                                        
                                else:
                                    print('ERROR: Invalid value, cannot be greater than sun up finish time!!')
                                    errorflash()
                            else:
                                print('ERROR: Invalid value')
                                errorflash()
                    elif selection == '2':
                        print('Sunrise Finish: ', upfinish)
                        update = str(input('New value? (24H):'))
                        if update != upfinish:
                            if 0 < int(update) <= 2359:
                                if update > upstart:
                                    if len(update) == 4:
                                        settingsupdate(update, upfinish, completestring)
                                        upfinish = update
                                    else:
                                        print('ERROR:Invalid value')
                                        errorflash()
                                else:
                                    print('ERROR: Invalid value, cannot be less that sun up start time!!')
                                    errorflash()
                            else:
                                print('ERROR: Invalid value')
                                errorflash()
                    elif selection == '3':
                        print('Sunset Start: ', setstart)
                        update = str(input('New value? (24H):'))
                        if update != setstart:
                            if 0 < int(update) <= 2359:
                                if update > setfinish:
                                    if len(update) == 4:
                                        settingsupdate(update, setstart, completestring)
                                        upfinish = update
                                    else:
                                        print('ERROR: Invalid value')
                                        errorflash()
                                else:
                                    print('ERROR: Invalid value, cannot be greater that sun down finish time!!')
                                    errorflash()
                            else:
                                print('ERROR: Invalid value')
                                errorflash()
                    elif selection == '4':
                        print('Sunset Finish: ', setfinish)
                        update = str(input('New value? (24H):'))
                        if update != setfinish:
                            if 0 < int(update) <= 2359:
                                if update > setstart:
                                    if len(update) == 4:
                                        settingsupdate(update, setfinish, completestring)
                                        setfinish = update
                                    else:
                                        print('ERROR: Invalid value')
                                        errorflash()
                                else:
                                    print('ERROR: Invalid value, cannot be less that sun down start time!!')
                                    errorflash()
                            else:
                                print('ERROR: Invalid value')
                                errorflash()
                    
                    elif selection == 'H':
                        print('These settings are the timers for the sunup and sundown functions.')
                        print('To amend, select the option to change and enter a new value for the hour in 24H format')
                        print('IMPORTANT: You need to include the 0 (ie 02 for 0200) or errors occur')
                        selection = 'F'
                        time.sleep(1)
                    elif selection == '0':
                        print('Exiting...')
                        selection = '0'
            elif selection == '2':
                while selection != '0':
                    print('1. Storm time:',stormtime)
                    print('2. Storm amount:', storms)
                    print('3. Storm length:', stormlength)
                    print('H - Help')
                    print('0 - Backup')
                    selection = 'F'
                    selection = str(input('Where to?:'))
                    if selection == '1':
                        update = str(input('What time do you want the storms?:'))
                        if update != stormtime:
                            if len(update) == 4:
                                if 0 <= int(update) <= 2359:
                                    settingsupdate(update, stormtime, completestring)
                                    stormtime = update
                                else:
                                    print('ERROR: Invalid value')
                                    errorflash()
                            else:
                                print('ERROR: Invalid value length')
                                errorflash()
                        else:
                            print('ERROR: Invalid value')
                            errorflash()
                    elif selection == '2':
                            print('Storm Settings: ', storms)
                            update = str(input('How many?: (0 is off)'))
                            if update != storms:
                                if int(update) <= 7:
                                    if len(update) != 2:
                                        update = '0'+update
                                    settingsupdate(update, storms, completestring)
                                    storms = update
                                else:
                                    print('ERROR: Too many! (Limited to 1 daily!')
                                    errorflash()
                    elif selection == '3':
                        print('Storm length:', stormlength)
                        update = str(input('How long? (60 is max): '))
                        if update != storms:
                            if 0 < int(update) <= 60:
                                if len(update) != 2:
                                        update = '0'+update
                                settingsupdate(update, stormlength, completestring)
                                stormlength = update
                            else:
                                print('ERROR: Too long! (60 mins top!)')
                                errorflash()
                    elif selection == 'H':
                        print('Select storm hour in 24H format (01 = 0100, 23 = 2300)')
                        print('Select how many days a storm should happen, up to 7')
                        print('Select how long the storm lasts, up to 60 mins')
                    elif selection == '0':
                        print('Exiting..')
                        #selection = 'F'
                       
                    
            elif selection == '3':
                print('Today: ',today)
                print('Now: ',now)


    def filehandling(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring):
        files = open("parameters.txt","r")
        upstart = files.readline()
        upstart = upstart[0:4]
        upfinish = files.readline()
        upfinish = upfinish[0:4]
        setstart = files.readline()
        setstart = setstart[0:4]
        setfinish = files.readline()
        setfinish = setfinish[0:4]
        stormtime = files.readline()
        stormtime = stormtime[0:4]
        storms = files.readline()
        storms = storms[0:2]
        stormlength = files.readline()
        stormlength = stormlength[0:2]
        files.close()
        files = open("parameters.txt","r")
        completestring = files.read()
        files.close()
        files = open("days.txt","r")
        stormdays = files.read()
        files.close()
        return upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring
    
    def buttonhandler():
        while exitflag != True:
            time.sleep(1)
            if GPIO.input(19) and GPIO.input(20):
                mainmenu()
            elif GPIO.input(20):
                print('Red')
            elif GPIO.input(21):
                print('Yellow')
        
    def settingsupdate(update, oldvalue, completestring):
        files = open("parameters.txt","w")
        completestring = completestring.replace(oldvalue,update)
        files.write(completestring)
        files.close()

    def randomday():
            x = random.randint(1, 7)
            return str(x)
    def timeparameters():
        while exitflag != True:
            global today
            global now
            today = int(datetime.date.today().strftime("%w"))
            now = int(datetime.datetime.now().strftime("%H%M"))
            time.sleep(60)
        #return today, now
            #^^ legacy return of the finction
    def errorflash():
        GPIO.output(25, GPIO.LOW)
        for i in range(0,5):
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.1)
        GPIO.output(25, GPIO.HIGH)
        
    # Define functions which animate LEDs in various ways.
    def colorWipe(strip, color, wait_ms=50):
            """Wipe color across display a pixel at a time."""
            for i in range(strip.numPixels()):
                    strip.setPixelColor(i, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    
    def stormLEDS(strip, color, wait_ms=50):
            for i in range(0, strip.numPixels(), 1):
                    strip.setPixelColorRGB(i, 255,0,0)
                    strip.show()
                    time.sleep(wait_ms/1000)
            
    #timerthread = threading.Thread(target=timeparameters)
    #timerthread.start()
    #LEDThread = threading.Thread(target=LEDRunner)
    #LEDThread.start()
    buttonThread = threading.Thread(target=buttonhandler)
    buttonThread.start()
    upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring = filehandling(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring)

    if int(storms) < 7:
        files = open("days.txt","r")
        stormholder = files.read()
        files.close()
        while int(storms) != len(stormholder):# #this is to add extra days to the random list or remove some, it doesnt currently work.
            files = open("days.txt","r")
            stormholder = files.read()
            files.close()
            files = open("days.txt","w")
            if int(storms) < len(stormholder):
                #for s in range(0,len(stormholder)-(int(storms))):
                stormholder = stormholder[0:int(storms)]
                print(stormholder)
                files.write(stormholder)
            elif int(storms) > len(stormholder):
                for s in range(0,int(storms)-(len(stormholder))):
                    extra = randomday()
                    for x in range(0,7):
                        for q in range(0,len(stormholder)): #check day isnt duplicated
                            if extra == stormholder[q]:
                               extra = randomday()
                               q = 0
                    stormholder = stormholder+extra
                    files.write(stormholder)
                    #print(stormholder)
            files.close()
        '''for i in range(0,len(stormholder)): #initialise the list
            stormdays.append(0)
        for i in range(0,len(stormholder)):
            stormdays[i] = int(stormholder[i])
            print(stormdays[i])'''
        stormdays = stormholder

    if today == 0:
        for p in range(0,int(storms)):
            extra = randomday()
            stormholder = stormholder+extra
    
    while exitflag == False:
        stormLEDS(strip, Color(0, 0, 255))
        #colorWipe(strip, Color(0, 255, 0))
        #colorWipe(strip, Color(0, 0, 255))
        if selection == '0':
            exitflag = True
            print('Shutting off everything (Can take up to 1 Minute)')
            

        
except KeyboardInterrupt:
    if selection == '0':
            exitflag = True
            print('Performing shutdown! Relaunch main.py or reboot pi the reinstate lights!')
    print('Exiting...')
    colorWipe(strip, Color(0, 0, 0))

finally:
    exitflag = True
    files.close()
    timerthread.join()
    #LEDThread.join()
    buttonThread.join()
    GPIO.output(25, GPIO.LOW)
    colorWipe(strip, Color(0, 0, 0))
    GPIO.cleanup()
    