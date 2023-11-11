# Arduino-Powered MIDI Stepper Motor Project

## Introduction

The goal of this project is to be able to import any MIDI file in to the software of your choice, and output them to the Arduino and use the attached stepper motors to act as frequency generators for some cool music.

## Prerequisites

Please read the entire tutorial before starting this project. You should also have a basic understanding of MIDI files and how they work. If you do not, I would recommend watching [this YouTube video](https://youtu.be/faZIkN_e_1s) before continuing.

<iframe width="1280" height="720" src="https://www.youtube.com/embed/faZIkN_e_1s" title="MIDI Explained for Beginners" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

This project requires some advanced understanding of electronics. You should be familiar with the Arduino board and how to upload sketches to it. You should also be familiar with basic Python programming and how to install Python libraries. The most complex thing will be troubleshooting motor issues (this is explained further in the troubleshooting section).
Do consider you may encounter problems that require you to search for solutions online. This project costs roughly $60-$70 to complete if you have none of the parts. You can find the parts list below.
This tutorial is for 4 motors but you can use as many as your microcontroller (the Arduino Duo in this case) supports. Each extra motor requires a minimum of 2 digitalOutput pins on the Arduino.

This project also requires the use of a DAW(Digital Audio Workstation) to convert the MIDI files to a format that can be used by the Python script. I used FL Studio for this but you can use any DAW **as long as you are able to output to a single MIDI port, with many MIDI channels**.

I have noted individual parts of the instructions that may be difficult to understand or may require some extra research. **I would very highly recommend figuring out how to solve the problems that do not cost anything before you buy anything.** It's much easier to bail on a project if you've not spent any money on it. The amazon links are affiliate links and I will get a small commission if you purchase through them. That being said, if you are able to find the same parts for cheaper elsewhere I would recommend doing that.

## Materials Needed

- [Arduino Duo](https://amzn.to/3ucQLEB)
- [Arduino CNC Shield](https://amzn.to/3swZSQ0) This comes with drivers so you do not have to purchase them separately.
- [NEMA 17 Stepper Motors (this link is a 5 pack for the best price)](https://amzn.to/3SEyPwC)
- [Driver modules for stepper motors (A4988 are good because they are loud)](https://amzn.to/3QQbbvP) You do not need this if you buy the CNC shield above, they are included with that.
- Paperclip or an electrical test lead - This is used to test the polarity of the motors
- [12V Power Supply](https://amzn.to/3SDBPJQ)

## Software Requirements

- [Arduino IDE](https://www.arduino.cc/en/software)
- MIDI Editor or DAW (I used FL Studio)
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
- [Python](https://www.python.org/downloads/) (Version doesn't matter too much, I used 3.11.3)

## Setup and Installation

### Arduino Setup

1. Install the Arduino IDE from the link above.
2. Connect the Arduino to your computer using the USB cable.
3. Open the Arduino IDE and select the correct board and port from the Tools menu.
   It should look something like this:

<img src="tutorial_images/Arduino_IDE.png">

4. You do not need to plug anything in to the Arduino yet. We will do that later.
5. You can test the Arduino by uploading the Blink sketch from the Examples menu. This will blink the onboard LED on the Arduino. If this works, you are ready to move on to the next step.

### Python Environment Setup

1. Install Python from the link above.

## Hardware Assembly

1. **Connecting Stepper Motors to Driver Modules**: Diagram and explanation.
2. **Wiring Motors to Arduino**: Step-by-step guide with diagrams.
3. **Power Supply Connections**: Safety and connection tips.

## Software Configuration

### Arduino Programming

1. **Loading the Stepper Motor Control Sketch**: Instructions to load and explain the code.
2. **Basic Motor Movement Test**: Test to ensure motors respond correctly.

### Python Scripting

1. **Python MIDI Script Overview**: Explain the purpose and functionality of your Python script.
2. **Running the Script**: Instructions on how to execute the Python script.

## Final Testing and Troubleshooting

- Guide on how to test the entire setup.
- Common issues and troubleshooting tips.

## Usage and Examples

- Detailed examples of how to use the system.
- Ideas for projects or experiments.

## Conclusion

Summarize what the user should have achieved and suggest further experiments or modifications.

## Additional Resources

- Links to helpful resources, forums, or further reading.
