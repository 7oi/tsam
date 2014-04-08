# ----------------------------------------------------------------- #
#                   TSAM Programming assignment nr.2                #
#                         Jóhann Fr. Jóhannsson                     #
# ----------------------------------------------------------------- #

import sys
import math

# ------------------- Defined helper functions -------------------- #

# I decided to make some helper functions
def netInfo (address, mask):     # To get network and broadcast address
    result = []
    result.append('')
    result.append('')
    addSplit = address.split('.')   # Make the list of numbers
    maskSplit = mask.split('.')     # ...same
    for i in range (0, 4):          # Loop and mask
        network = int(addSplit[i]) & int(maskSplit[i])   # & the nrs
        broadcast = int(addSplit[i]) | (~int(maskSplit[i]) & 255)
        result[0] += str(network)        # add to string
        result[1] += str(broadcast)   # add to string
        if i < 3:
            result[0] += '.'           # Forget the last dot!
            result[1] += '.'
    return result

# This function counts the bits in the mask, assuming it's properly entered
def maxHosts (mask):
    maskSplit = mask.split('.')
    result = 0
    for i in range (0, 4):
        result += bin(int(maskSplit[i])).count('1')
    result = 32 - result        # I want the number of leftover bits
    return str((2 ** result) - 2)

# This function checks the class
def classCalc (address):        # To figure out the class
    addSplit = address.split('.')   # Split the address up
    addrClass = int(addSplit[0]) & 192 # Figure out class
    if (addrClass == 192):      
        return 'C'      # Class
    elif (addrClass == 128):        
        return 'B'
    else:
        return 'A'


# ---------------------- The printing part ----------------------- #

addr = sys.argv[1]      # Take cmd line arguments 1 and 2
msk = sys.argv[2]

addresses = netInfo(addr, msk)
printout = 'This host is part of the following network: '
printout += addresses[0]
printout += '\nMaximum number of hosts on the network: '
printout += maxHosts(msk)
printout += '\nBroadcast address: '
printout += addresses[1]
printout += '\nNetwork class: '
printout += classCalc(addr)
print(printout)
