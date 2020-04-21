#!/bin/bash
powertop --workload="python3 $1" --csv=powerOut.csv
cat powerOut.csv | grep python | grep ms > energyTime.txt
echo "Outputted filtered powertop results to 'energyTime.txt'"
