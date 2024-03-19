## [Reading from Force Gauages]([https://asmedigitalcollection.asme.org/appliedmechanics/article/88/5/051010/1099667/Implicit-Contact-Model-for-Discrete-Elastic-Rods](https://www.qualityforcegauges.com/force-gauges/fb-precision?gad_source=1&gclid=CjwKCAjw7-SvBhB6EiwAwYdCAY0_omCXQO2mvaEX3uhxheVIBawPpJJ9_6UMmkbzvYosYaOmkr-vNBoCBuAQAvD_BwE)https://www.qualityforcegauges.com/force-gauges/fb-precision?gad_source=1&gclid=CjwKCAjw7-SvBhB6EiwAwYdCAY0_omCXQO2mvaEX3uhxheVIBawPpJJ9_6UMmkbzvYosYaOmkr-vNBoCBuAQAvD_BwE)

This repo contains a script used to record the force gauge data via USB directly. It has been tested on Torbal FB Series gauges on both Linux and windows systems. However, it should work for any force sensor that can connect to computers via USB cables. This instruction is written based on the usage of Torbal FB Series.

## How to Use
### Dependencies
Install the latest python first:
- [python](https://www.python.org/downloads/)
  - python is used for executing the script contained in this repo
  - The script is tested for python 3.12

- Required python packages
  - ```pyserial```: Pyserial encapsulates the access for the serial port.
  - ```matplotlib```: Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
  - Installation commands:
    ```bash
    pip3 install pyserial matplotlib
    ```
    
### Instructions
Set up the environment for using the script correctly:
- Adjust the configuration of force gauge
  - Open the ```menu``` of the force gauge.
  - Navigate to the ```configuration```
  - Navigate to the ```Interface```
  - Select ```USB mode```
  - Select a broad rate value ```#X```, keep that value
  - Select the data mode to ```continous```.

- Adjust the computer environment (Linux):
  - Open the terminal
  - Input ```lsusb``` to decide the port name ```$PORT_NAME``` of for the force gauge.
  - Grant the write and read permission for this port: ```sudo chmod a+rw $PORT_NAME```
    
- Adjust the computer environment (Windows) (Note this can be also followed the [Chapter 16](https://mytorbal.com/download/207/fb-fc-instruction-manualpdf):
  - Open the ```device manager```
  - Navigate to ```Ports (COM & LPT)
  - Find the USB serial Port (COM) for the force gauge
  - Change the broad rate of the port to ```#X```

### Usage
  - Run the script ```python3 force_gauage_reading.py```







