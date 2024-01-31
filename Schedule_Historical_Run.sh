#!/bin/sh
source /home/raspberrypi/Daikin-SkyFi-AirCon/venv/bin/activate
cd /home/raspberrypi/Daikin-SkyFi-AirCon
/home/raspberrypi/Daikin-SkyFi-AirCon/venv/bin/python /home/raspberrypi/Daikin-SkyFi-AirCon/get_aircon_stats.py 
deactivate
