from WSEN_PDUS import WSEN_PDUS

print('This script will test the differential pressure and temperature sensor')
print('This sensor uses I2C to communicate, which is not testable with simply a multimeter')
print('For this test, we will use known setups to check for proper functionality')
print('')

dP_sensor = WSEN_PDUS()

print('For the first test, do not connect any tubes to sensor')
print('The differential pressure should read approximately 0')
print('The temperature will read room temperature')

print('')

dP, temp = dP_sensor.getPressureAndTemperature()

print('The differential pressure is ', dP, ' kPa')
print('The temperature is ', temp, ' *C')

if dP > 0.1:
    print('The sensor is reading a large differential pressure')
    print('Double check that no air flow is connected')

if temp < 16:
    print('The temperature is reading very cold, are you in a refrigerator?')

if temp > 27:
    print('The temperature is reading very warm')

print('')
print('Now, check that it works reasonably in situ')
print('Set up the venturi with the handheld manometer and flow air through it')
print('Note the differential pressure reading')
print('DO NOT turn off the air flow after reading')

print('')
input('Press Enter to continue...')

print('')
print('While leaving the airflow on, disconnect the manometer from the venturi')
print('Connect the tubes to the differential pressure sensor')
print('Note that the inputs are sensitive to the direction of air flow')
print('One is labeled for higher pressure and one for lower')

print('')
input('Press Enter to continue...')

print('')

dP, temp = dP_sensor.getPressureAndTemperature()

print('The differential pressure is ', dP, ' kPa')
print('The temperature is ', temp, ' *C')

print('')
print('If the differential pressure is reasonably close to the manometer reading, great!')
print('If it is not, try reconnecting the manometer to see if something changed')