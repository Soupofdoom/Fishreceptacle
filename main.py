try:    
    from neopixel import *
    import RPi.GPIO as GPIO
    import time
    import datetime
    import threading
    #--------------------GPIO Config
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(19, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(21, GPIO.IN)
    
    # LED strip configuration:
    LED_COUNT      = 60     # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0
    LED_STRIP      = ws.SK6812_STRIP_RGBW

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
   
    # Define functions which animate LEDs in various ways.
    def colorWipe(strip, color, wait_ms=50):
            """Wipe color across display a pixel at a time."""
            for i in range(strip.numPixels()):
                    strip.setPixelColor(i, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
    def wheel(pos):
            """Generate rainbow colors across 0-255 positions."""
            if pos < 85:
                    return Color(pos * 3, 255 - pos * 3, 0)
            elif pos < 170:
                    pos -= 85
                    return Color(255 - pos * 3, 0, pos * 3)
            else:
                    pos -= 170
                    return Color(0, pos * 3, 255 - pos * 3)	
    def rainbow(strip, wait_ms=20, iterations=1):
            """Draw rainbow that fades across all pixels at once."""
            for j in range(256*iterations):
                    for i in range(strip.numPixels()):
                            strip.setPixelColor(i, wheel((i+j) & 255))
                    strip.show()
                    time.sleep(wait_ms/1000.0)
    
    def colourblend(strip,start,finish,palette):
        length = (int(finish) - int(start))
        if length >= 100:
            length = length * 0.6
        length = length * 60
        n = 100 # number of steps in the blend, more is smoother but tends to reduce the update time to unrealistic times and causes extra time on blends or runaways
        updateinterval = float((length/(n * len(palette))))
        if updateinterval < 1:
            updateinterval = 0.1 # prevents a runaway colour train or update intervals of 0
            
        
        f = 0
        #updateinterval = 0.01 # debug line, saves waiting >10mins for transisitons
        for y in range(0,(len(palette))):
            #print(len(palette))
            #print(y)
             
            f = 0
            while f < n:
                #print(y) # y gives out of range @ 2? wtf? Now it doesn't
                if y == (len(palette)-1):
                    endpoint = y
                    break
                    #print('Complete colours')
                    #print('Y = len palette - 1 = 0')
                else:
                    endpoint = y+1
                    #print('y+1',endpoint)
                first = overrun(palette[y][0] + (palette[endpoint][0]-palette[y][0]) * f / n)
                second = overrun(palette[y][1] + (palette[endpoint][1]-palette[y][1]) * f / n)
                third = overrun(palette[y][2] + (palette[endpoint][2]-palette[y][2]) * f / n)
                fourth = overrun(palette[y][3] + (palette[endpoint][3]-palette[y][3]) * f / n)
                #print(first,second,third,fourth) #debug line
                for x in range(strip.numPixels()):
                    #print(first,second,third,fourth)
                    #strip.setPixelColor(x,Color(palette[y][0],palette[y][1],palette[y][2],palette[y][3]))
                    strip.setPixelColor(x,Color(first,second,third,fourth))
                
                
                strip.show()
                
                time.sleep(updateinterval)
                f += 1
            #time.sleep(updateinterval)
    
    def brightnesschange(start,finish):
        global now
        global exitflag
        length = ((int(finish) - int(start)) * 0.6) *60
        interval = length/255
        '''while exitflag != True:#start < now < finish:
            for x in range(0,255):
                strip.setBrightness(overrun(x))
                print(x)
                if exitflag == True:
                    break
                time.sleep(interval)'''        
        
    #------------------- Other non light related functions
    def overrun(checking):
        if checking < 0:
            checking = 0
            #True = True
        if checking > 255:
            checking = 255
            #False = False
        return checking
    
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
        validatesettings(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring)
        return upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring
    
    def validatesettings(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring):
        #clarify rules and regs for timers
        if int(upfinish) - int(upstart) < 10: #never less than 10 because time.sleep cannot cope with it
            print('Sunrise is too short!')
            #update setting with user input
        if int(setfinish) - int(setstart) < 10:
            print('Sunset is too short!')
        #etc etc
            
    def settingsupdate(update, oldvalue, completestring):
        files = open("parameters.txt","w")
        completestring = completestring.replace(oldvalue,update)
        files.write(completestring)
        files.close()
        
    def timeparameters(): #Monitors the time and day in a seperate thread (started at line
        while exitflag != True:
            global today
            global now
            today = str(datetime.date.today().strftime("%w"))
            now = str(datetime.datetime.now().strftime("%H%M"))
            
            time.sleep(60) #Here be dragons! Removing this line causes a system wide crash due to resources being consumed. Even a 1 second sleep has a meltdown.
    
    def errorflash():
        GPIO.output(25, GPIO.LOW)
        for i in range(0,5):
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.1)
        GPIO.output(25, GPIO.HIGH)
    
    def buttonhandler():
        while exitflag != True:
            time.sleep(1)
            if GPIO.input(20) and GPIO.input(21):
                print('Both')
            elif GPIO.input(20):
                print('Red')
            elif GPIO.input(21):
                print('Yellow')
            elif GPIO.input(19):
                print('Green?')
    
    def color_to_RGB(color):
        #hopefully
        return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
    #--------Misc setup
    exitflag = False
    #--------------------Variable Declaration
    today = 0
    now = 0    
    upstart = 0
    upfinish = 0
    setstart = 0
    setfinish = 0
    stormtime = 0
    storms = 0
    stormlength = 0
    completestring = 0 #if i dont declare these it doesnt like the next line?
    upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring = filehandling(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring)
    
    #Thread launching
    timerthread = threading.Thread(target=timeparameters)
    timerthread.start()
    #buttonThread = threading.Thread(target=buttonhandler)
    #buttonThread.start()
    
    #Setupcomplete
    
    GPIO.output(25, GPIO.HIGH) 
    print('Setup Complete, initiating lighting')
    #---------ACTUAL PROGRAM
    count = 0
    #print(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength, completestring)
    sunrisecolours = [[0,0,0,0],[255,0,0,128],[0,255,0,25],[0,0,255,255],[24,50,65,38],[10,129,254,8],[255,255,255,255]] #start with 0 & end with 255 for sun coming up, vice versa for down
    sunsetcolours = [[255,255,255,255],[0,0,125,255],[0,0,0,0]]
    #validate whether time and sunrise makes sense then set flag
    
    sunriseflag = False
    sunsetflag = False
    daytimeflag = False
    
    while exitflag != True:
        if int(upfinish) < int(now):
            sunriseflag = True
            daytimeflag = True
        if int(setfinish) < int(now):
            sunsetflag = True
            daytimeflag = False
        #rainbow(strip, wait_ms=20,iterations=1)
        if int(upstart) <= int(now) <= int(upfinish) and sunriseflag == False:
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Sunrise')
            colourblend(strip,upstart,upfinish,sunrisecolours)
            sunriseflag = True
            daytimeflag = True
            sunsetflag = False
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Sunrise finish')
        elif int(setstart) <= int(now) <= int(setfinish) and sunsetflag == False:
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Sunset start')
            colourblend(strip, setstart, setfinish, sunsetcolours)
            sunsetflag = True
            daytimeflag = False
            sunriseflag = False
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Sunset finish')
        elif daytimeflag == True:
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Daytime')
            for x in range(strip.numPixels()):
                    #print(first,second,third,fourth)
                    #strip.setPixelColor(x,Color(palette[y][0],palette[y][1],palette[y][2],palette[y][3]))
                
                    strip.setPixelColor(x,Color(255,255,255,255))
                
                
            strip.show() #setdark
        else:
            print(int(datetime.datetime.now().strftime("%H%M")))
            print('Nighttime')
            for x in range(strip.numPixels()):
                    #print(first,second,third,fourth)
                    #strip.setPixelColor(x,Color(palette[y][0],palette[y][1],palette[y][2],palette[y][3]))
                    strip.setPixelColor(x,Color(0,0,0,0))
                
                
            strip.show()#setlight
            time.sleep(60) # change this from 60 when going live
        #print(count)
        count += 1
       


except KeyboardInterrupt:
    print('Exiting...')
    exitflag = True
finally:
    GPIO.output(25, GPIO.LOW)
    for x in range(0,3):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(1/4)
        GPIO.output(23, GPIO.LOW)
        time.sleep(1/4)
    #colorWipe(strip, Color(255, 0, 0))
    colorWipe(strip, Color(0, 0, 0))
    GPIO.cleanup()
    