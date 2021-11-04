## Running the code
On MacOS and Ubuntu, open the terminal, `cd` to this `sofrware` directory, and enter
```
python3 main.py
```
On Windows, open the CMD, `cd` to this `sofrware` directory, and enter
```
py main.py
```
If you want to run the code without connecting an Arduino, you can add "--simulation":
```
python3 main.py --simulation
```
## Understand the code
### Code Structure
- `main.py` is entry point of the software.

- `control/widgets.py` implements the widget classes, the widgets, when instantiated, are the interface between the user and the code execution. 

- `control/core.py` implements classes of objects that gets the work done. These objects do not directly interacts with the user but through widgets implemented. In this example, since we're just turning on/off the LED through a button, we did not implement a class for this simple task. If we were to follow the pattern used in the octopi/squid codebase, we'd create an LEDController class, that contains a function that can be called by the widget to turn on/off the LED.

- `control/microcontroller.py` implements the communication methods between the microcontroller and the software, and abstract the micontroller hardware as an object that the software can directly interact with (e.g. a `set_LED_state` function is implemented that can be directly called) 

- `control/_def.py` difines constants used in the code, e.g. length of the command packet (in bytes) that's sent to the microcontroller through the serial interface.

- `control/gui.py` is what connects everything together. It create the gui class, that will be instantiated by `main.py`. Within the class, widgets and other objects that constitute the code are instantiated and linked together, either through passing references of objects (e.g. `self.ledControlWidget = widgets.LEDControlWidget(self.microcontroller)`, or by connecting signals and slots using the `connect` method.
### Explanation of the code
#### `main.py`
The following line is the most relevant line in the code. Set `is_simulation` to `True` if no hardware is connected.
```
win = gui.OctopiGUI(is_simulation=False)
```
#### `control/widgets.py`
`class LEDControlWidget(QFrame)` define the class for the LED control widget. It inherits from QFrame so that the widget can have the appearance of a frame, which can be inserted into the GUI.

```
def __init__(self, microcontroller, main=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.microcontroller = microcontroller
        self.add_components()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
```

`def __init__(self, microcontroller, main=None, *args, **kwargs)` defines how the widget will be initialized when instantiated, for example, when `example_widget = LEDControlWidget(mcu)` is called, where `mcu` is an microcontroller object, which will be discussed later.

`self.microcontroller = microcontroller` makes the microcontroller object passed to the `__init__` function - when the widget object is being created  part of the widget object, as an "data attribute" ("instance variable" in Smalltalk terminology and "data member" in C++ terminology). To be more explict, it's the reference to the microcontroller object that is passed along, which helps understand why the same object can be "pass on" to or be "part" of many different objects.

`self.add_components()` is called to set up various aspects of the widget (Qt GUI elements and their connections to functions). This function is defined below and its use is to make the `__init__` function visually uncluttered.

```
def add_components(self):
    self.btn_led = QPushButton("ON/OFF")
    self.btn_led.setCheckable(True)
    self.btn_led.setChecked(False)
    self.btn_led.setDefault(False)

    grid_line0 = QGridLayout()
    grid_line0.addWidget(QLabel('LED'), 0,0)
    grid_line0.addWidget(self.btn_led, 0,1)

    self.grid = QGridLayout()
    self.grid.addLayout(grid_line0,0,0)
    self.setLayout(self.grid)

    self.btn_led.clicked.connect(self.set_LED_state)
```

In `add_components(self)`, a button *widget* is created and its attributes are set (first four lines of the function defination). A gird *layout* is then created (`grid_line0 = QGridLayout()`) to lay out a lable widget (`grid_line0.addWidget(QLabel('LED'), 0,0)`) and the button widget just created (`grid_line0.addWidget(self.btn_led, 0,1)`). Then the layout is set as *the layout* of the LEDControlWidget widget that is being defined. The last line `self.btn_led.clicked.connect(self.set_LED_state)` connects the *signal* `clicked` of the button, which will be *emitted* when the button is clicked, to the function `set_LED_state` that's defined below, so that clicking of the button leads to the execution of the `set_LED_state` function.

```
def set_LED_state(self,pressed):
    self.microcontroller.set_LED_state(pressed)
```
The above function instruct the "referenced" microcontroller to execute its `set_LED_state` function.
