# HEader:
# PID    COMMAND          %CPU TIME     #TH   #WQ #PORTS MEM   PURG  CMPRS PGRP  PPID  STATE    BOOSTS     %CPU_ME %CPU_OTHRS UID FAULTS   COW     MSGSENT   MSGRECV   SYSBSD    SYSMACH   CSW       PAGEINS IDLEW   POWER INSTRS CYCLES USER               #MREGS RPRVT VPRVT VSIZE KPRVT KSHRD
import energyusage

def main():
    energyusage.evaluate(test)

def test():
    a = -0
    while(a < 200):
        a += 1
    
    
if __name__ == '__main__':
    main()
    