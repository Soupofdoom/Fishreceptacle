import datetime
import random

def randomday():
        x = random.randint(1, 7)
        #if x == 1:
           # print('Monday')
        #elif x==2:
           # print('Tuesday')
        #elif x==3:
           # print('Wednesday')
        #elif x==4:
           # print('Thursday')
        #elif x==5:
           # print('Friday')
        #elif x==6:
           # print('Saturday')
        #elif x==7:
           # print('Sunday')
        #else:
           # print('Error')
        return x
today =datetime.date.today().strftime("%w")
whatday = 0
if today == '1':
    whatday = randomday()
    
print('Today:', today)
print(whatday)
print('end')
