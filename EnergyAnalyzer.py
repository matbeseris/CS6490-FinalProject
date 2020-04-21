# This file will run the various Bluetooth connection methods
# and analyize their power consumption, comparing and printing results
import sys
import os
from KeyExchanges import DHERSA, DHAPSK
from CipherMethods import AES, ChaCha20


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
        str = f.read()
        str = str.split(" ms/s")[0]
        msOutput.append(str)
        i+=1
    
    
    # Print energy rating of each program
    i = 0
    print("*** Result energy ratings (higher = more energy used) *** ")
    while(i < len(msOutput)):
        print(sys.argv[i+1] + ":\t " + msOutput[i])
	i+=1
    

if __name__ == '__main__':
    main()