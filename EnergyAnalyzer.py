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
    i = 1
    while(i < len(sys.argv)):
        os.system("sudo ./analyzeEnergy.sh " + sys.argv[i])
        # Filtered output is in energytime.txt
        i+=1
    

if __name__ == '__main__':
    main()