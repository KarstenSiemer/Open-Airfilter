import time
from ccs811.CCS811_RPi import CCS811_RPi
from ccs811.SDL_Pi_HDC1000 import SDL_Pi_HDC1000, HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT, HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT
#import SDL_Pi_HDC1000 # comment this line if you don't use HDC sensor
#from CCS811_RPi import CCS811_RPi

ccs811 = CCS811_RPi()

# Do you want to use integrated temperature meter to compensate temp/RH (CJMCU-8118 board)?
# If not pre-set sensor compensation temperature is 25 C and RH is 50 %
# You can compensate manually by method ccs811.setCompensation(temperature,humidity)
HDC1080         = True

'''
MEAS MODE REGISTER AND DRIVE MODE CONFIGURATION
0b0       Idle (Measurements are disabled in this mode)
0b10000   Constant power mode, IAQ measurement every second
0b100000  Pulse heating mode IAQ measurement every 10 seconds
0b110000  Low power pulse heating mode IAQ measurement every 60
0b1000000 Constant power mode, sensor measurement every 250ms
'''
# Set MEAS_MODE (measurement interval)
configuration = 0b100000

#print 'MEAS_MODE:',ccs811.readMeasMode()
ccs811.configureSensor(configuration)

# Use these lines if you use CJMCU-8118 which has HDC1080 temp/RH sensor
if(HDC1080):
        hdc1000 = SDL_Pi_HDC1000()
        hdc1000.turnHeaterOff()
        hdc1000.setTemperatureResolution(HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
        hdc1000.setHumidityResolution(HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)

        humidity = hdc1000.readHumidity()
        temperature = hdc1000.readTemperature()
        ccs811.setCompensation(temperature,humidity)

statusbyte = ccs811.readStatus()
print('STATUS: ', bin(statusbyte))

error = ccs811.checkError(statusbyte)
if(error):
        print('ERROR:',ccs811.checkError(statusbyte))

if(not ccs811.checkDataReady(statusbyte)):
        print('No new samples are ready')

result = ccs811.readAlg();

if(not result):
        print('Invalid result received');

print('eCO2: ',result['eCO2'],' ppm');
print('TVOC: ',result['TVOC'], 'ppb');
print('---------------------------------');
