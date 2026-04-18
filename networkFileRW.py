#!/usr/bin/env python3
#networkFileRW.py
#Pamela Brauda
#Thursday, March 3, 2022
#Update routers and switches;
#read equipment from a file, write updates & errors to file
#
#GPA 8 Modifications:
# - Added try/except clause for importing the JSON module
# - Added file constants for input files (equip_r.txt, equip_s.txt)
#   and output files (updated.txt, invalid.txt)
# - Used json.load() to read router and switch data from files into dictionaries
# - Used json.dump() to write updated device dictionary to updated.txt
# - Used json.dump() to write invalid IP address list to invalid.txt

try:
    import json
except ImportError:
    print("Error: JSON module could not be imported.")
    raise

# File constants
ROUTERS_FILE = "equip_r.txt"
SWITCHES_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERRORS_FILE = "invalid.txt"

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount
        
def main():

    # Open and read router file
    with open(ROUTERS_FILE, 'r') as rFile:
        routers = json.load(rFile)

    # Open and read switch file
    with open(SWITCHES_FILE, 'r') as sFile:
        switches = json.load(sFile)

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # Write updated dictionary to file
    with open(UPDATED_FILE, 'w') as uFile:
        json.dump(updated, uFile)
    print("Updated equipment written to file 'updated.txt'")

    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write invalid IP list to file
    with open(ERRORS_FILE, 'w') as eFile:
        json.dump(invalidIPAddresses, eFile)
    print("List of invalid addresses written to file 'invalid.txt'")

#top-level scope check
if __name__ == "__main__":
    main()