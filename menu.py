def mainmenu(selection):
    #filehandling(upstart, upfinish, setstart, setfinish, stormtime, storms, stormlength)
    while selection != 0:  
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
                    update = input('New value? (24H):')
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
                    update = input('New value? (24H):')
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
                    update = input('New value? (24H):')
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
                    update = input('New value? (24H):')
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
                                errorflash()
                        else:
                            print('ERROR: Invalid value length')
                            errorflash()
                    else:
                        print('ERROR: Invalid value')
                        errorflash()
                elif selection == '2':
                        print('Storm Settings: ', storms)
                        update = input('How many?: (0 is off)')
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
                    update = input('How long? (60 is max): ')
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
                   
                
        elif selection == '3':
            print('Today: ',today)
            print('Now: ',now)
