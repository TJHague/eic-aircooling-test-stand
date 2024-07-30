import RPi.GPIO as GPIO
from digitalio import DigitalInOut

class CS_MUX:
    pins = []
    cs_pin = None

    ch_max = 16

    class CS_MUX_pin(DigitalInOut):
        mux = None
        ch = None
        def __init__(self, 
                    mux,
                    ch: int):
            self.mux = mux
            self.ch = ch
        
        def switch_to_output(self, value, drive_mode):
            pass

        def switch_to_input(self, pull):
            pass

        @property
        def value(self, value: int):
            self.mux.toggle(self.ch, value)

    def __init__(self, pins: list[int], cs_pin: int):
        # GPIO.setmode(GPIO.BOARD)

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
    
    def select_out(self, ch: int) -> None:
        if ch >= self.ch_max:
            raise ValueError("Multiplexer does not have enough pins to output to channel {:d}".format(ch))
        
        for i, pin in enumerate(self.pins):
            GPIO.output(pin, (ch >> i) & 1)
        
        GPIO.output(self.cs_pin, 0)
    
    def deselect(self) -> None:
        GPIO.output(self.cs_pin, 1)

    def toggle(self, ch: int, cs_out: int | bool) -> None:
        if cs_out == 0 or cs_out == False:
            self.select_out(ch)
        elif cs_out == 1 or cs_out == True:
            self.deselect()
        else:
            raise ValueError("Pin can only be high or low. Function accepts integers of 0 and 1 or booleans")
    
    def get_CS_pin(self, ch: int) -> CS_MUX_pin:
        return self.CS_MUX_pin(self, ch)

    def __del__(self):
        GPIO.cleanup()
