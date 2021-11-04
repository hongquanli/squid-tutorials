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
Use one of the following to start the program
```
python3 main.py
python3 main_camera_only.py
python3 main_motion_only.py
```
To start the program when no hardware is connected, use
```
python3 main_simulation.py
```
