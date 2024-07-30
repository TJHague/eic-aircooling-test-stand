import board
from CS_MUX import CS_MUX
import RPi.GPIO as GPIO  

# GPIO.setmode(GPIO.BOARD)

mux_pins_default = [17, 27, 22, 23]
mux_cs_default = 24

mux = CS_MUX(pins = mux_pins_default, cs_pin = mux_cs_default)

print('Multiplexer Pins:')
for p, i in enumerate(mux_pins_default):
    print('S', i, ' - Pin ', p)

print('')
print('Sig - Pin ', mux_cs_default)

print('------')
print('')
print('First, check that signal pin')
print('It should be low, 0 V')

mux.select_out(0)

input("Press Enter to continue...")

print('')
print('Now the signal pin should be high, 3.3 V')

mux.deselect()

input("Press Enter to continue...")

print('')
print('------')
print('')
print('Now checking multiplexer channel select and output pins')
print('Note: Standard CS for SPI defaults to HI when deselected and LO when selected')
print('For the purposes of this test script, it is assumed that the signal pins are disconnected from their respective boards.')
print('This code then sets the signal to HI (3.3 V) for ease of measurement.')
print('')
print('------')

for i in range(16):
    print('Check that the mux channel select pins read: ')
    for p, j in enumerate(mux_pins_default):
        print('Pin ', p, ' - Value ', (i>>j) & 1)
    print('')
    print('Check that signal output ', i, ' is HI, 3.3V')

    mux.select_out(i)
    GPIO.output(mux_cs_default, 1)

    input("Press Enter to continue...")

mux.deselect()

print('')
print('------')
print('')
print('All channels have now been checked. If any of the outputs do not read correctly, investigate the connections.')
exit()