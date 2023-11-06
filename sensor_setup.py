import board
import adafruit_max31865
import WSEN_PDUS.WSEN_PDUS as dP_T_sensor


def setup_pt100s(nPT100s, pins=None):
    """Sets up PT100s for reading in main program. If only nPT100s is used, it defaults to using predefined GPIO pins. Can also be passed an list of GPIO pins to be used.

    Args:
        nPT100s (int): Number of PT100s to set up. Ignored if pins are passed.
        pins (list[board.pin], optional): List of GPIO pins to use for setting up PT100s. Defaults to None.

    Raises:
        TypeError: Raised if nPT100s is not an integer. Will not raise if pins is set.
        ValueError: Raised if nPT100s is negative. Will not raise if pins is set.
        ValueError: Raised if nPT100s is larger than the default list of GPIO pins. Will not raise if pins is set.

    Returns:
        list[adafruit_max31865.MAX31865]: A list of set up interfaces that can be used to read each PT100.
    """
    spi = board.SPI()
    if pins is not None:
        return [
            adafruit_max31865.MAX31865(
                spi,
                pin,
                rtd_nominal=100,
                ref_resistor=400,
                wires=2,
                filter_frequency=60,
                polarity=0,
            )
            for pin in pins
        ]

    # GPIO pins available for use
    # Not fully populated, just starting with a few for testing
    # Sensors should be connected in the order of this array
    cs_pins = [
        board.D5,
        board.D6,
        board.D13,
        board.D19,
        board.D26,
        board.D12,
        board.D16,
        board.D20,
    ]

    if type(nPT100s) is not int:
        raise TypeError("nPT100s must be an integer")
    if nPT100s < 0:
        raise ValueError("Cannot have negative number of PT100s")
    if nPT100s > len(cs_pins) + 1:
        raise ValueError(
            "Too many PT100s - {} is the maximum when relying on default pin configuration".format(
                len(cs_pins) + 1
            )
        )

    return [
        adafruit_max31865.MAX31865(
            spi,
            cs_pins[i],
            rtd_nominal=100,
            ref_resistor=400,
            wires=2,
            filter_frequency=60,
            polarity=0,
        )
        for i in range(nPT100s)
    ]


def setup_pressure_and_temperature_sensors(nSensors=1, i2c_channels=NotImplemented):
    """Sets up differential pressure and temperature sensors. Currently only allows for a single sensor.
    TODO: Set up software i2c so that more than 1 may be used.

    Args:
        nSensors (int, optional): Number of sensors using default setup. Currently overrides to 1 as software i2c is not yet implemented. Defaults to 1.
        i2c_channels (list of ints, optional): List of i2c channes to use. Currently ignored as software i2c is not yet implemented. Defaults to NotImplemented.

    Returns:
        list of WSEN_PDUS type sensors : list of differential pressure and temperature sensors. Will always be length 1 until software i2c is implemented.
    """
    if nSensors != 1:
        nSensors = 1

    return [dP_T_sensor() for _ in range(nSensors)]
