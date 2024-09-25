import smbus
import time

class WSEN_PDUS:
    """WSEN_PDUS class. This class sets up an interface via i2c between a Raspberry Pi and a Wurth Elektronik WSEN PDUS differential pressure and temperature sensor. At the time of writing, this only works for board number 2513254510291 with sensor number 2513130810201.
    Currently it uses hardware i2c only, restricting it to only a single sensor due to all sensors having identical i2c addresses.
    This code is, more or less, a direct translation of the code provided by the manufacturer into python.

    TODO: Implement software i2c

    Raises:
        ValueError: An instance of the class must be initialized before data can be read as the i2c connection is created at initialization
    """

    i2c_address = 0x78

    pressure_min = 3277
    temperature_min = 8192

    def __init__(self, i2c_channel=1):
        """Initializes a Raspberry PI to WSEN_PDUS connection. Currently only implemented for hardware i2c
        TODO: Implement software i2c

        Args:
            i2c_channel (int, optional): i2c channel to use. Currently overrides anything sent to use hardware i2c. Defaults to 1.
        """
        # Force the use of hardware i2c
        # Software i2c will be implemented at a later time
        if i2c_channel != 1:
            i2c_channel = 1
        self.i2c = smbus.SMBus(i2c_channel)
        time.sleep(0.5)

    def read_data(self):
        """Reads 4 bytes of data from the WSEN PDUS board. The first two bytes are differential pressure, the second two bytes are temperature.
        TODO: Handle read failures

        Raises:
            ValueError: This can only be done from an initialized instance of the class, as that sets up the i2c connection

        Returns:
            list of 4 bytes: two bytes of raw differential pressure, second two bytes of raw temperature.
        """
        if self.i2c is None:
            raise ValueError("i2c not initialized")
        return self.i2c.read_i2c_block_data(self.i2c_address, 0, 4)

    def convert_pressure_data(self, data):
        """Converts raw differential pressure data to kPa

        Args:
            data (list of bytes): A list of bytes, this assumes that the first two bytes are the raw differential pressure data

        Returns:
            float: Differential pressure in kPa
        """
        P = (data[0] << 8) | data[1]
        P = P - self.pressure_min
        P = ((P * 7.63) / 10000) - 10
        return P

    def convert_temperature_data(self, data):
        """Converts raw temperature data to *C

        Args:
            data (list of bytes): A list of bytes, this assumes that the first two bytes are the raw temperature data (i.e. the raw differential pressure data has been stripped from the beginning of the list)

        Returns:
            float: Temperature in *C
        """
        T = (data[0] << 8) | data[1]
        T = T - self.temperature_min
        T = (T * 4.272) / 1000
        return T

    def getPressure(self):
        """Return the differential pressure in kPa. Note that this forces a read action with the WSEN_PDUS.

        Returns:
            float: Differential pressure in kPa
        """
        data = self.read_data()
        return self.convert_pressure_data(data[:2])

    def getTemperature(self):
        """Returns the temperature in *C. Note that this forces a read action with the WSEN_PDUS.

        Returns:
            float: Temperature in *C
        """
        data = self.read_data()
        return self.convert_temperature_data(data[2:])

    def getPressureAndTemperature(self):
        """Returns a tuple of the differential pressure in kPa and temperature in *C. Note that this forces a read action with the WSEN PDUS.

        Returns:
            tuple of 2 floats : Differential pressure in kPa, Temperature in *C
        """
        data = self.read_data()
        return self.convert_pressure_data(data[:2]), self.convert_temperature_data(
            data[2:]
        )
