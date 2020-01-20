import os.path
import datetime

logname = str('log/log-%s.txt'%datetime.datetime.now().strftime('%m-%d-%Y-%I-%M-%S'))

def log(inx):
    #Generate log header based on date/time
    mmt = datetime.datetime.now()
    #Get date variables
    yr = str(mmt.year)
    mt = str(mmt.month)
    dy = str(mmt.day)
    #Get time variables
    hr = str(mmt.hour)
    mn = str(mmt.minute)
    sc = str(mmt.second)
    ms = str(mmt.microsecond)

    #Convert certain variables to 2-characters if needed
    if len(yr)>2:
        yr = yr[-2]
    if len(mt)==1:
        mt = "0" + mt
    if len(dy)==1:
        dy = "0" + dy
    if len(hr)==1:
        hr = "0" + hr
    if len(mn)==1:
        mn = "0" + mn
    if len(sc)==1:
        sc = "0" + sc

    #Finalize entry beginning
    ent = yr + mt + dy + "." + hr + ":" + mn + ":" + sc + ":" + ms + ": " + str(inx) + "\n"
    
    print(logname)
    #Check if log file already exists
    if os.path.isfile(logname):
        #Log file exists
        fx = open(logname, "a")
    else:
        #Need to create log file
        fx = open(logname, "x")

    #Write to the file
    try:
        fx.write(ent)
    except err as error:
        print(err)
    finally:
        fx.close()