import time
import datetime
import random
import threading
#Welcome to hell.....
#Still to do:
# Random day selection and storage
exitflag = False
#------------------------------------file handling start
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
#-------------------------------- file handling finish / variables begin
today = 0
now = 0
stormdays = []
selection = 'F'

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
    #return today, now
        #^^ legacy return of the finction

timerthread = threading.Thread(target=timeparameters)
timerthread.start()

randomflag = False
if int(storms) < 7:
    files = open("days.txt","r")
    stormholder = files.read()
    files.close()
    while int(storms) != len(stormholder):# #this is to add extra days to the random list or remove some, it doesnt currently work.
        files = open("days.txt","r+")
        stormholder = files.read()
        if int(storms) > len(stormholder):
            for s in range(0,(int(storms)-len(stormholder))):
                stormholder = stormholder[0:int(storms)]
                print(stormholder)
                files.write(stormholder)
        elif int(storms) < len(stormholder):
            for s in range(0,(len(stormholder)-int(storms))):
                extra = randomday()
                stormholder = stormholder+extra
                files.write(stormholder)
                print(stormholder)
    for i in range(0,len(stormholder)): #initialise the list
        stormdays.append(0)
    for i in range(0,len(stormholder)):
        stormdays[i] = int(stormholder[i])
        print(stormdays[i])
    stormdays = stormdays.sort()    

while exitflag == False:
    print('Main Menu:')
    print('1. Timer Settings')
    print('2. Storm Settings')
    print('3. Timer output')
    print('0 - Shutdown')
    selection = input('Where to?: ')
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
            selection = input('Where to? ')
    
            if selection == '1':
                print('Sunrise start: ', upstart)
                update = input('New value? (24H):')
                if update != upstart:
                    if 0 < int(update) <= 2359:
                        if update < upfinish:
                            if len(update) == 4:
                                settingsupdate(update, upstart, completestring)
                                upstart = update
                            else:
                                print('ERROR:Invalid value')
                        else:
                            print('ERROR: Invalid value, cannot be greater than sun up finish time!!')
                    else:
                        print('ERROR: Invalid value')
            elif selection == '2':
                print('Sunrise Finish: ', upfinish)
                update = input('New value? (24H):')
                if update != upfinish:
                    if 0 < int(update) <= 2359:
                        if update > upstart:
                            if len(update) == 4:
                                settingsupdate(update, upfinish, completestring)
                                upfinish = update
                            else:
                                print('ERROR:Invalid value')
                        else:
                            print('ERROR: Invalid value, cannot be less that sun up start time!!')
                    else:
                        print('ERROR: Invalid value')
            elif selection == '3':
                print('Sunset Start: ', setstart)
                update = input('New value? (24H):')
                if update != setstart:
                    if 0 < int(update) <= 2359:
                        if update > setfinish:
                            if len(update) == 4:
                                settingsupdate(update, setstart, completestring)
                                upfinish = update
                            else:
                                print('ERROR: Invalid value')
                        else:
                            print('ERROR: Invalid value, cannot be greater that sun down finish time!!')
                    else:
                        print('ERROR: Invalid value')
            elif selection == '4':
                print('Sunset Finish: ', setfinish)
                update = input('New value? (24H):')
                if update != setfinish:
                    if 0 < int(update) <= 2359:
                        if update > setstart:
                            if len(update) == 4:
                                settingsupdate(update, setfinish, completestring)
                                setfinish = update
                            else:
                                print('ERROR: Invalid value')
                        else:
                            print('ERROR: Invalid value, cannot be less that sun down start time!!')
                    else:
                        print('ERROR: Invalid value')
            
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
            selection = input('Where to?:')
            if selection == '1':
                update = input('What time do you want the storms?:')
                if update != stormtime:
                    if len(update) == 4:
                        if 0 <= int(update) <= 2359:
                            settingsupdate(update, stormtime, completestring)
                            stormtime = update
                        else:
                            print('ERROR: Invalid value')
                    else:
                        print('ERROR: Invalid value length')
                else:
                    print('ERROR: Invalid value')
            elif selection == '2':
                    print('Storm Settings: ', storms)
                    update = input('How many?: (0 is off)')
                    if update != storms:
                        if int(update) <= 7:
                            settingsupdate(update, storms, completestring)
                            storms = update
                        else:
                            print('ERROR: Too many! (Limited to 1 daily!')
            elif selection == '3':
                print('Storm length:', stormlength)
                update = input('How long? (60 is max): ')
                if update != storms:
                    if 0 < int(update) <= 60:
                        settingsupdate(update, stormlength, completestring)
                        stormlength = update
                    else:
                        print('ERROR: Too long! (60 mins top!)')
            elif selection == 'H':
                print('Select storm hour in 24H format (01 = 0100, 23 = 2300)')
                print('Select how many days a storm should happen, up to 7')
                print('Select how long the storm lasts, up to 60 mins')
            elif selection == '0':
                print('Exiting..')
               
            
    elif selection == '3':
        print('Today: ',today)
        print('Now: ',now)
    elif selection == '0':
        exitflag = True
        print('Performing shutdown! Relaunch main.py or reboot pi the reinstate lights!')
files.close()
timerthread.join()