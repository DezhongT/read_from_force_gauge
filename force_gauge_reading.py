import serial
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt

def try_convert_to_float(s):
    try:
        return float(s)
    except ValueError:
        return 0.0


ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc} [{hwid}]")

# port = "/dev/ttyUSB0"
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout = 1)

time_data = []
force_data = []

start_time = time.time()
while time.time() - start_time < 15:
    line = ser.readline().decode().strip()
    res = try_convert_to_float(line)
    time_data.append(time.time() - start_time)
    force_data.append(res)
    print(res)

plt.clf()
plt.plot(time_data, force_data)
plt.xlabel("Time, t [s]")
plt.ylabel("Force, F [N]")
plt.pause(0.03)

plt.show()
