## Setting up the environments

### install software dependencies
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pyqtgraph
sudo apt-get install python3-pyqt5
pip3 install qtpy pyserial
```
### install camera drivers
If you're using The Imaging Source cameras, follow instructions on https://github.com/TheImagingSource/tiscamera 

If you're using Daheng cameras, follow instructions in the `drivers and libraries/daheng camera` folder

## Using the software
Use the following command to start the program in simulation mode
```
python3 main.py --simulation
```
To run the program with hardware connected, use the following
```
python3 main.py
```
Below is a screenshot of the software in simulation mode
![alt text](https://i.imgur.com/9A46CFu.png)

## Full software
Full software under active development can be found at https://github.com/hongquanli/octopi-research

## Understanding the code
To understand the structure of the code, refer to https://github.com/hongquanli/squid-tutorials/tree/main/example_led_control/software. After that the code here should be self-explanatory. 
