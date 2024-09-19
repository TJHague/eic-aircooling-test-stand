import RPi.GPIO as GPIO
from digitalio import DigitalInOut

class CS_MUX:
    """CS_MUX class. Used to distribute a single SPI chip select signal to multiple devices, reducing the need for a large number of GPIO pins. It is currently set up with a maximum of 4->16 pins, as that is what is currently used. Should a new multiplexer be used in the future, this should be easily changeable by adjusting the ch_max variable.

    ### Raises:
        - `ValueError`: Raises ValueError if an output pin greater than ch_max is selected
        - `ValueError`: Raises ValueError if user attempts to set chip select pin to anything other than on or off
    """
    pins = []
    cs_pin = None

    ch_max = 16

    class CS_MUX_pin(DigitalInOut):
        """CS_MUX_pin class. A child class of digitalio.DigitalInOut. Allows passing the pin to classes that expect a DigitalInOut for controlling direct connections to the Raspberry Pi. This overloads the 'value' property in order to call the CS_MUX functions properly.
        """
        mux = None
        ch = None
        def __init__(self, 
                    mux,
                    ch: int):
            self.mux = mux
            self.ch = ch
        
        def switch_to_output(self, value, drive_mode):
            """## switch_to_output Unused"""
            pass

        def switch_to_input(self, pull):
            """## switch_to_input Unused"""
            pass

        @property
        def value(self, value: int):
            """## value Reimplementation to call the underlying CS_MUX function

            ### Args:
                - `value (int)`: value to set the pin to
            """
            self.mux.toggle(self.ch, value)

    def __init__(self, pins: list[int], cs_pin: int):
        """## __init__ Sets up the multiplexer. Ensures that the maximum number of outputs is consistent with the number of input pins.

        ### Args:
            - `pins (list[int])`: List of input GPIO pins to use as output selectors
            - `cs_pin (int)`: GPIO pin that is used as chip select
        """
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
        """## select_out Select a channel to output to and pull the chip select pin LOW

        ### Args:
            - `ch (int)`: Output channel number

        ### Raises:
            - `ValueError`: Raises ValueError if an output pin greater than ch_max is selected
        """
        if ch >= self.ch_max:
            raise ValueError("Multiplexer does not have enough pins to output to channel {:d}".format(ch))
        
        for i, pin in enumerate(self.pins):
            GPIO.output(pin, (ch >> i) & 1)
        
        GPIO.output(self.cs_pin, 0)
    
    def deselect(self) -> None:
        """## deselect Pulls the chip select pin HI (default for no communication)
        """
        GPIO.output(self.cs_pin, 1)

    def toggle(self, ch: int, cs_out: int | bool) -> None:
        """## toggle Turn a multiplexer output on or off, based on the value of cs_out. Effectively a wrapper of select_out() and deselect() into a single function.

        ### Args:
            - `ch (int)`: Output channel number
            - `cs_out (int | bool)`: Select or deselect the channel ch

        ### Raises:
            - `ValueError`: Raises ValueError if user attempts to set chip select pin to anything other than on or off
        """
        if cs_out == 0 or cs_out == False:
            self.select_out(ch)
        elif cs_out == 1 or cs_out == True:
            self.deselect()
        else:
            raise ValueError("Pin can only be high or low. Function accepts integers of 0 and 1 or booleans")
    
    def get_CS_pin(self, ch: int) -> CS_MUX_pin:
        """## get_CS_pin Returns a 'CS_MUX_pin' for a specific output channel to allow another code to control the pin without implementing the underlying multiplexer codes

        ### Args:
            - `ch (int)`: Channel to return pin for

        ### Returns:
            - `CS_MUX_pin`: Pin that behaves like a digitalio.DigitalInOut pin.
        """
        return self.CS_MUX_pin(self, ch)

    def __del__(self):
        """## __del__ destructor"""
        GPIO.cleanup()
