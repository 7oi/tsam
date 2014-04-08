# ----------------------------------------------------------------- #
# Client program:                                                   #
# Client can send messages to server where they will be processed.  #
# Then receives messages from server like directory listings        #
# and error messages.                                               #
# Doesn't really do much more than that.                            #
# Using Python v3.3.2                                               #                                                                  #
# ----------------------------------------------------------------- #

from socket import *

sn = input('Input server name (default: localhost):')
serverPort = input('Select port (default: 12000):')      # Default port
if sn == '':   # If Return, set to localhost
    sn = '127.0.0.1'
if serverPort == '':
    serverPort = 12000
try:    # Try to connect to server.
    getaddrinfo(sn, int(serverPort))
    serverName = sn # Choose server
except: # If connection fails, connect to localhost
    serverName = '127.0.0.1'
    print ('Error: No such server. Setting to localhost')
clientSocket = socket(AF_INET, SOCK_STREAM) # Setting up
clientSocket.connect((serverName, int(serverPort)))
path = clientSocket.recv(1024)
# Now to print instructions on screen
print('Connected to server! \n\n' +
      'To list items in directory type "show dir" \n' +
      'To browse type "cd", followed by folder name or .. for parent\n' +
      'To quit, type q/Q\n' +
      'To quit and kill server, type "kill server"\n')
s = input('So... Where to?\n' + path.decode() + '> ') # Print current path
while 1:    # Loop until conditionals inside are true
    try:
        clientSocket.send(s.encode())
        modifiedS = clientSocket.recv(1024)
        print (modifiedS.decode())
    except:
        print ('Error: Connection not responding. Might be closed')
        break
    
    # Commands to close client and kill server
    if s == 'q' or s == 'Q' or s == 'kill server':  
        break
    path = clientSocket.recv(1024)
    s = input(path.decode() + '> ' )    # Print current path again
clientSocket.close()
