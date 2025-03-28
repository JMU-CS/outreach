# Finch Robot Dance Party

!!! abstract "Learning Objectives"
    *After today's activity, you should be able to:*

    * Program a finch robot to move around and change colors.
    * Summarize three methods provided by a finch robot object.
    * Define a function with no parameters and no return value.


## Getting Started

The original finch is a robot designed for computer science education.
Watch the video below to get an idea of how the finch works.
Also take a few minutes to learn about the [finch hardware][2].

<iframe width="600" height="340" frameborder="0" allowfullscreen
src="https://www.youtube.com/embed/MBT5BrIBMoE"></iframe>

To connect to a finch robot from Python, you will need two files:

1. The `finch` module (written in Python):
    * :material-file-code: [finch.py](finch.py)
2. A USB driver for your operating system:
    * :material-file-cog: [libhidapi64.so](libhidapi64.so) -- Linux
    * :material-file-cog: [libhidapi.dylib](libhidapi.dylib) -- macOS
    * :material-file-cog: [hidapi64.dll](hidapi64.dll) -- Windows

!!! warning

    These files won't work on Chromebooks and newer Macs (M1, M2).
    However, you can run the finch module using a web browser.
    See the finch [installation instructions][3] for details.

[1]: https://store.birdbraintechnologies.com/products/finch-robot
[2]: https://learn.birdbraintechnologies.com/resources/finch-hardware/
[3]: https://learn.birdbraintechnologies.com/finch1/python/install/


## Example Code

``` py title="dance.py" linenums="1"
import finch
import time

# connect to the Finch robot
robot = finch.Finch()

# green light, move forward
robot.led(0, 255, 0)
robot.wheels(0.75, 0.75)
time.sleep(1.5)

# turn off lights and wheels
robot.halt()
```

The first line imports the [finch module](finch.py), and the second line imports the built-in [time module][4].
You will use `finch` to control the finch robot and `time` to control the program's timing.

Line 5 creates a `Finch` object and assigns a reference to `robot`.
If you have multiple robots, you can call `finch.Finch()` multiple times to connect to each robot:

``` py
romeo = finch.Finch()
juliet = finch.Finch()
```

Lines 8--10 turn on the LED, turn on the wheels, and pause the program for 1.5 seconds.
After `time.sleep()` returns, Line 13 turns off the LED and both wheels.
Note the following details:

* `robot.led(red, green, blue)` -- values range from 0 to 255; see Google's [color picker][5].
* `robot.wheels(left, right)` -- values range from -1.0 to +1.0 and represent percentages.
* `time.sleep(sec)` -- controls how long the program will wait before running the next line.

[4]: https://docs.python.org/3/library/time.html
[5]: https://www.google.com/search?q=color+picker
