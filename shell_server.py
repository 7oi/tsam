# ----------------------------------------------------------------- #
#   Server program.                                                 #
#   Can return directory listing of C:\temp with filesizes          #
#   Can also browse between directories and catches exceptions      #
#   
#

import os
import datetime
from socket import *

# Make a function to return current time for logging
def currentTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Setting up
serverPort = 12000      # Default server port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready')
logFile = open(os.getcwd() + '\\TSAM_serverLog.txt', 'a')  # Make/open a log file
logFile.write('\n\n' + currentTime() + ' : Server started\n')   # Start logging
while 1:    # Loop until server receives kill command
    s = ''  #   Preset the variables
    connectionSocket, addr = serverSocket.accept()
    print (currentTime() + ' : Connection from '+ str(addr))
    logFile.write('\n' + currentTime() + ' : Connection from ' + str(addr) + '\n')
    while 1:    # Loop until server receives quit or kill command
        path = os.getcwd()
        connectionSocket.send (path.encode())
        msg = bytes('  ', 'utf-8')
        logg = ''
        s = connectionSocket.recv(1024)
        s = s.decode()  # We receive bytes, so str needs to be decoded
        if s == 'show dir':     # This command lists the items in the directory
            try:
                for filename in os.listdir(path):
                    temp = '{:30} {:16} {:9}'.format(filename, os.path.getsize(path + '\\' + filename), ' bytes\n')
                    msg = msg + temp.encode()   # Making a string with the directory listing
                logg = currentTime() + ' : Showed dir at ' + path + ' ' + str(addr)
            except:
                msg = bytes('Error: cannot access directory', 'utf-8')
                logg = currentTime() + ' : Failure to access ' + path + ' ' +  str(addr)
        elif s[0:2] == 'cd':    # This command moves between directories
            if s[2:4] == '..':
                os.chdir(path[0:path.rfind('\\')])
                logg = currentTime() + ' : Moved to ' + os.getcwd() + ' ' +  str(addr)
            else:
                try:
                    os.chdir(path + '\\' + s[3:])
                    logg = currentTime() + ' : Moved to ' + os.getcwd() + ' ' +  str(addr)
                except:
                    msg = bytes('Error: no such directory!\n', 'utf-8')
                    logg = currentTime() + ' : Fail! Tried to access non existent directory. LOL! ' + str(addr)
            
        elif s == 'q' or s == 'Q':
            connectionSocket.send (bytes('Thank you. Goodbye!', 'utf-8'))
            logg = currentTime() + ' : Closed the connection ' + str(addr)
            print (logg)
            logFile.write(logg + '\n')
            connectionSocket.close ()
            break
        elif s == 'kill server':
            connectionSocket.send (bytes('Thank you. Goodbye!', 'utf-8'))
            logg = currentTime() + ' : Closed the connection and killing the server ' + str(addr)
            print (logg)
            logFile.write(logg + '\n')
            break
        else:
            msg = bytes('No such command!', 'utf-8')
            logg = currentTime() + " : Fail! Client doesn't know the commands. LOL! " + str(addr)
        connectionSocket.send (msg)
        print (logg)
        logFile.write(logg + '\n')
    if s == 'kill server':
        break
connectionSocket.close ()
logFile.write(currentTime() + ' : Server down\n')
logFile.close()
