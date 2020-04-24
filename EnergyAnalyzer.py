# This file will run the various Bluetooth connection methods
# and analyize their power consumption, comparing and printing results
import sys
import os
import subprocess

def main():
    if(len(sys.argv) == 1):
        print("Please enter at least 1 command line argument of the python program to run.")
        exit(0)
        
    # Run each of the scripts
    msOutput = []
    i = 1
    while(i < len(sys.argv)):
        os.system("sudo ./analyzeEnergy.sh " + sys.argv[i])
        # Filtered output is in energytime.txt
        f = open("energyTime.txt")
        str = f.readline()
        values = str.split(";")
        if len(values) == 0:
            msOutput.append("")
        elif len(values) == 7:
            msOutput.append(values[6] + "\t" + values[0] + "\t" + values[-1])
        else:
            msOutput.append(values[6] + "\t" + values[0])
        i+=1
    
    
    # Print energy rating of each program
    i = 0
    print("*** Result energy ratings (higher = more energy used) *** ")
    while(i < len(msOutput)):
        print(sys.argv[i+1] + ":\t " + msOutput[i])
        i+=1
    

if __name__ == '__main__':
    main()
