from sensor_setup import air_cooling_test_stand
import time

test_stand = air_cooling_test_stand()

for _ in range(10):
    heater_temps = test_stand.get_pt100_temperatures()
    air_temps = test_stand.get_thermocouple_temperatures()
    dPs = test_stand.get_dP_and_T()

    print("PT100 Temperatures:")
    for i,pt in enumerate(heater_temps):
        print("PT100 #{}: {} *C".format(i,pt))

    print("\n")
    print("Thermocouple Temperatures:")
    for i,t in enumerate(air_temps):
        print("Thermocouple #{}: {} *C".format(i,pt))

    print("\n")
    print("Differential Pressure Sensor Readings:")
    for i, dP_T in enumerate(dPs):
        print("Sensor {}: {} kPa, {} *C".format(i, dP_T[0], dP_T[1]))

    time.sleep(1)

# dP_sensors = sensor_setup.setup_pressure_and_temperature_sensors()

# for _ in range(12):
#     for i in range(len(dP_sensors)):
#         dP, T = dP_sensors[i].getPressureAndTemperature()
#         print("Sensor {} reads:".format(i))
#         print("  Differential Pressure: {} kPa".format(dP))
#         print("  Temperature:           {} *C".format(T))
#         print("\n---\n")