import board
import adafruit_max31865
import adafruit_max31855
import WSEN_PDUS
from CS_MUX import CS_MUX

class air_cooling_test_stand:
    spi = None
    mux = None
    pt100s = None
    thermocouples = None
    dPs = None
    mux_pins_default = [17, 27, 22, 23]
    mux_cs_default = 24
    
    def __init__(self, mux_pins: list[int] = mux_pins_default, mux_cs: int = mux_cs_default, nPT100s: int = 10, nThermocouples: int = 2, ndPs: int = 1):
        if len(mux_pins) > 4:
            raise ValueError(
                "The multiplexer is limited to 16 channels, so the number of control pins are limited to 4."
            )
        if nPT100s + nThermocouples > 2**(len(mux_pins)):
            raise ValueError(
                "More PT100s and Thermocouples than the multiplexer can support. With this number of multiplexer pins, only {} SPI devices can be used.".format(2**(len(mux_pins)))
            )
        self.mux = self.setup_MUX(mux_pins, mux_cs)
        self.pt100s = self.setup_pt100s([i for i in range(nPT100s)])
        self.thermocouples = self.setup_thermocouples([i + nPT100s for i in range(nThermocouples)])
        self.dPs = self.setup_pressure_and_temperature_sensors(nSensors = ndPs)

    def setup_MUX(pins: list[int] = mux_pins_default, cs: int = mux_cs_default) -> CS_MUX:
        return CS_MUX(pins = pins, cs_pin = cs)

    # With MUX, it seems that we likely don't need the number of SPI devices passed, just the MUX channels for them
    # Leaving the lines here for now in case I realize I was mistaken, but will probably delete later
    # def setup_thermocouples(nThermocouples: int, MUX: CS_MUX, MUX_IDs: list[int]) -> list[adafruit_max31855.MAX31855]:
    def setup_thermocouples(MUX: CS_MUX, MUX_IDs: list[int]) -> list[adafruit_max31855.MAX31855]:
        spi = board.SPI()
        return [
            adafruit_max31855.MAX31855(spi, MUX.get_CS_pin(pin))
            for pin in MUX_IDs
        ]

    # def setup_pt100s(nPT100s: int, MUX: CS_MUX, MUX_IDs: list[int]) -> list[adafruit_max31865.MAX31865]:
    def setup_pt100s(MUX: CS_MUX, MUX_IDs: list[int]) -> list[adafruit_max31865.MAX31865]:
        """Sets up PT100s for reading in main program. If only nPT100s is used, it defaults to using predefined GPIO pins. Can also be passed an list of GPIO pins to be used.

        Args:
            nPT100s (int): Number of PT100s to set up. Ignored if pins are passed.
            MUX_IDs (list[int]): List of MUX channels to use for setting up PT100s.

        Raises:
            TypeError: Raised if nPT100s is not an integer. Will not raise if pins is set.
            ValueError: Raised if nPT100s is negative. Will not raise if pins is set.
            ValueError: Raised if nPT100s is larger than the default list of GPIO pins. Will not raise if pins is set.

        Returns:
            list[adafruit_max31865.MAX31865]: A list of set up interfaces that can be used to read each PT100.
        """

        # if type(nPT100s) is not int:
        #     raise TypeError("nPT100s must be an integer")
        # if nPT100s < 0:
        #     raise ValueError("Cannot have negative number of PT100s")
        # if nPT100s > len(MUX_IDs) + 1:
        #     raise ValueError(
        #         "Too many PT100s - {} is the maximum when relying on default pin configuration".format(
        #             len(MUX_IDs) + 1
        #         )
        #     )

        spi = board.SPI()
        return [
            adafruit_max31865.MAX31865(
                spi,
                MUX.get_CS_pin(pin),
                rtd_nominal=100,
                ref_resistor=400,
                wires=2,
                filter_frequency=60,
                polarity=0,
            )
            for pin in MUX_IDs
        ]

        # # GPIO pins available for use
        # # Not fully populated, just starting with a few for testing
        # # Sensors should be connected in the order of this array
        # cs_pins = [
        #     board.D5,
        #     board.D6,
        #     board.D13,
        #     board.D19,
        #     board.D26,
        #     board.D12,
        #     board.D16,
        #     board.D20,
        # ]



        # return [
        #     adafruit_max31865.MAX31865(
        #         spi,
        #         cs_pins[i],
        #         rtd_nominal=100,
        #         ref_resistor=400,
        #         wires=2,
        #         filter_frequency=60,
        #         polarity=0,
        #     )
        #     for i in range(nPT100s)
        # ]


    def setup_pressure_and_temperature_sensors(nSensors=1, i2c_channels=NotImplemented) -> list[WSEN_PDUS.WSEN_PDUS]:
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
            print("Software currently only functional for a single differential pressure sensor. Only 1 will be set up.")

        return [WSEN_PDUS.WSEN_PDUS() for _ in range(nSensors)]
    
    def get_pt100_temperatures(self) -> list[float]:
        return [pt100.temperature for pt100 in self.pt100s]
    
    def get_thermocouple_temperatures(self) -> list[float]:
        return [thermocouple.temperature_NIST for thermocouple in self.thermocouples]

    def get_dPs(self) -> list[float]:
        return [dP.getPressure() for dp in self.dPs]
    
    def get_dP_and_T(self) -> list[tuple[float, float]]:
        return [dP.getPressureAndTemperature() for dP in self.dPs]