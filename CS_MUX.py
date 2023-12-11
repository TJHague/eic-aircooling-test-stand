import RPi.GPIO as GPIO

class CS_MUX:
    pins = []
    cs_pin = None

    ch_max = 16

    def __init__(self, pins, cs_pin):
        GPIO.setmode(GPIO.BOARD)

        # Set the output pin
        # In this implementation, it is the chip select that will be passed to the breakout boards
        # CS should be high when not reading
        self.cs_pin = cs_pin
        GPIO.setup(cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, 1)

        if len(pins) > 4:
            del pins[4:]
        if len(pins) < 4:
            self.ch_max = 2**len(pins)

        for pin in pins:
            self.pins.append(pin)
            GPIO.setup(pin, GPIO.OUT)
    
    def select_out(self, ch):
        if ch >= self.ch_max:
            raise ValueError("Multiplexer does not have enough pins to output to channel {:d}".format(ch))
        
        for i, pin in enumerate(self.pins):
            GPIO.output(pin, (ch >> i) & 1)
        
        GPIO.output(self.cs_pin, 0)
    
    def deselect(self):
        GPIO.output(self.cs_pin, 1)

    def toggle(self, ch, cs_out):
        if cs_out == 0 or cs_out == False:
            self.select_out(ch)
        elif cs_out == 1 or cs_out == True:
            self.deselect()
        else:
            raise ValueError("Pin can only be high or low. Function accepts integers of 0 and 1 or booleans")
    
    def __del__(self):
        GPIO.cleanup()