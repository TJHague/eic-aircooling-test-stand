import sensor_setup
import WSEN_PDUS

dP_sensors = sensor_setup.setup_pressure_and_temperature_sensors()

for _ in range(12):
    for i in range(len(dP_sensors)):
        dP, T = dP_sensors[i].getPressureAndTemperature()
        print("Sensor {} reads:".format(i))
        print("  Differential Pressure: {} kPa".format(dP))
        print("  Temperature:           {} *C".format(T))
        print("\n---\n")