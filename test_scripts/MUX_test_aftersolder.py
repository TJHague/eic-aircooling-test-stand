import board
from CS_MUX import CS_MUX
import RPi.GPIO as GPIO  

# This code checks the MUX output rather than the signal pins
# Effectively the same code, but the prompts are tailored for that check

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
print('First, check the signal pin')
print('It should be LO, 0 V')

mux.select_out(0)

input("Press Enter to continue...")

print('')
print('Now the signal pin should be HI, 3.3 V')

mux.deselect()

input("Press Enter to continue...")

print('')
print('------')
print('')
print('Now checking multiplexer channel select and output pins')
print('Note: Standard CS for SPI floats to HI when deselected and is pulled LO when selected')
print('This test script assumes that the MUX output channels are connected to their respective breakout boards.')
print('')
print('------')

print('First, check all of the MUX outputs')
print('Those that are connected to breakout boards should read HI, 3.3V')
print('Those that are not connected to breakout boards should be checked for continuity to ground, there should be no connection.')
print('')
print('Of particular importance to check at this step is output C0')
print('At the time of writing this code (Sep 25, 2024), the MUX enable pin is not implemented')
print('This has the effect that the last used output, C0 at startup, is driven HI rather than floated HI when output is deselected.')
print('In a perfect setup, the enable pin would be implemented and used when deselecting')
print('For this use case, it is likely unnecessary')

input('Press Enter after checking the output pins...')

print('')
print('------')
print('Now we move on to checking that output pins are properly selected')
print('This will step through each channel and pull it LO')
print('Also check that the previous channel is floated HI')
print('If the previous channel is not connected to a breakout board, it should instead read as disconnected from ground')

print('')
print('------')


for i in range(16):
    print('')
    print('------')
    print('Check that signal output C', i, ' is LO, 0V')
    if i!=0:
        print('Check that signal output C', i-1, 'is HI, 3.3V, or disconnected from GND')

    mux.select_out(i)

    input("Press Enter to continue...")

mux.deselect()

print('')
print('------')
print('')
print('All channels have now been checked. If any of the outputs do not read correctly, investigate the connections.')
exit()