## Running demo
First, follow the instructions in `firmware` folder to set up and program the microcontroller.

On MacOS and Ubuntu, open the terminal, `cd` to the `sofrware` directory, and enter
```
python3 main.py
```
On Windows, open the CMD, `cd` to the `sofrware` directory, and enter
```
py main.py
```
## Understand the code
### Software code Structure
- `main.py` is entry point of the software.

- `control/widgets.py` implements the widget classes, the widgets, when instantiated, are the interface between the user and the code execution. 

- `control/core.py` implements classes of objects that gets the work done. These objects do not directly interacts with the user but through widgets implemented. In this example, since we're just turning on/off the LED through a button, we did not implement a class for this simple task. If we were to follow the pattern used in the octopi/squid codebase, we'd create an LEDController class, that contains a function that can be called by the widget to turn on/off the LED.

- `control/microcontroller.py` implements the communication methods between the microcontroller and the software, and abstract the micontroller hardware as an object that the software can directly interact with (e.g. a `set_LED_state` function is implemented that can be directly called) 

- `control/_def.py` difines constants used in the code, e.g. length of the command packet (in bytes) that's sent to the microcontroller through the serial interface.

- `control/gui.py` is what connects everything together. It create the gui class, that will be instantiated by `main.py`. Within the class, widgets and other objects that constitute the code are instantiated and linked together, either through passing references of objects (e.g. `self.ledControlWidget = widgets.LEDControlWidget(self.microcontroller)`, or by connecting signals and slots using the `connect` method.
