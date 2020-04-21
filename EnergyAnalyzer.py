# This file will run the various Bluetooth connection methods
# and analyize their power consumption, comparing and printing results
from KeyExchanges import DHERSA, DHAPSK
from CipherMethods import AES, ChaCha20
import energyusage


def recursive_fib(n):
    if (n <= 2): return 1
    else: return recursive_fib(n-1) + recursive_fib(n-2)
    
def main():
    energyusage.evaluate(recursive_fib, 40, pdf=True)
    




if __name__ == '__main__':
    main()