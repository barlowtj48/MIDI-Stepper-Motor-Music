try:
    import mido
    import serial
except:
    print("Please install the required libraries using pip:")
    print("pip install mido")
    print("pip install pyserial")
    # This seems to be some dependency of mido that is undocumented
    print("pip install python-rtmidi")
    quit()

# These libraries are included with Python, you do not need to install them
import time
import re
import sys

# Constants for the MIDI to frequency conversion
A4_KEY = 69
# WOAH 440? Please express your preference with the variable below
# https://emastered.com/blog/432-hz-tuning-standard
A4_FREQ = 440

# The port that the Arduino is connected to
# It is input using command line arguments
# If you would like to debug this using VSCode, change the "args" value in .vscode/launch.json
if len(sys.argv) > 1:
    arduino_port = sys.argv[1]
else:
    print("Please specify the port that the Arduino is connected to.")
    print("For example:\npython midi_interface.py COM3")
    quit()

# If the second command line argument is "pitch_bending", enable pitch bending
# This enables the velocity of the note to change the frequency of the motor
# This is helpful when accounting for a few notes that are out of tune
# If the MIDI file is not out of tune, do not use this option
pitch_bending = False
if len(sys.argv) > 2 and sys.argv[2] == "pitch_bending":
    pitch_bending = True
    print("Pitch bending enabled.")


# The baud rate is the speed of the serial connection
# It must match the baud rate in the Arduino code
baud_rate = 115200
motor_channels = 0

# Open serial connection to Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
except:
    print("Serial connection failed. Please check your port and try again.")
    quit()

# Wait for Serial to initialize
time.sleep(3)

# Read from the serial to determine how many motors are connected
start_time = time.time()
# Wait for 5 seconds or until the we can set the number of motor channels
while motor_channels == 0 and time.time() - start_time < 5:
    try:
        channels_str = str(ser.readline().decode())
        channel_match = re.search(r'motors: (\d+)', channels_str)
        if channel_match is not None and channel_match.group(1) is not None:
            motor_channels = int(channel_match.group(1))
            # send "ack" to Arduino to enable the interface
            ser.write(b'ack\n')
            print(f"Script connected to Arduino with {motor_channels} motors.")
    except:
        print("Serial read failed. Please check your port and try again.")
        quit()

# Keeps track of which channels are outputting
channel_outputting = [False] * motor_channels

last_midi_activity_time = time.time()
motors_enabled = True  # The motors are enabled by default


def note_to_frequency(note):
    global pitch_bending
    """Convert a MIDI note number to a frequency in Hertz."""
    freq = A4_FREQ * 2 ** ((note - A4_KEY) / 12)
    if pitch_bending:
        # This will add 5 cent of pitch bending for every 1 velocity
        freq += freq * ((msg.velocity / 12700) * 5)
    return freq


def send_buffer_to_arduino(msg_buffer):
    """Send a buffer of MIDI messages to the Arduino over serial, all at once."""
    global channel_outputting, motors_enabled, last_midi_activity_time
    # Pretty print the buffer as columns of frequencies for each channel
    print_str = ""
    data_values = [0] * motor_channels
    for msg in msg_buffer:
        if msg['channel'] > motor_channels - 1:
            continue
        if msg['type'] == 'note_on':
            val = f"{msg['freq']:.2f}"
            if val == "0":
                val = "0.00"
            data_values[msg['channel']] = val
        elif msg['type'] == 'note_off':
            data_values[msg['channel']] = "0.00"
    for value in data_values:
        print_str += f"{value}\t"
    print(print_str)

    serial_data = b''
    for msg in msg_buffer:
        if msg['channel'] > motor_channels - 1:
            continue
        # If the channel is already outputting, end the previous note
        if channel_outputting[msg['channel']] and msg['type'] == 'note_on':
            # end the previous note
            serial_data += f'e,{msg["channel"]}\n'.encode()
            # start the new note
            serial_data += f's,{msg["channel"]},{msg["freq"]}\n'.encode()
        else:
            if msg['type'] == 'note_on':
                if not motors_enabled:
                    motors_enabled = True
                channel_outputting[msg['channel']] = True
                serial_data += f's,{msg["channel"]},{msg["freq"]}\n'.encode()
            elif msg['type'] == 'note_off':
                channel_outputting[msg['channel']] = False
                serial_data += f'e,{msg["channel"]}\n'.encode()
    try:
        last_midi_activity_time = time.time()
        ser.write(serial_data)
    except:
        print("Serial Write Failure. Was the device unplugged?")
        quit()


def disable_motors():
    """Send stop signal to all motors."""
    global motors_enabled, channel_outputting
    if not motors_enabled:
        return
    # if any of the channels are outputting, just return
    if any(channel_outputting):
        return
    print("5 second input timeout. Temporarily disabling motors.")
    motors_enabled = False
    data = b'd\n'
    try:
        ser.write(data)
    except:
        print("Serial Write Failure. Was the device unplugged?")
        quit()


# Print out available MIDI ports
# print(mido.get_input_names())

# Find the port that has "loopMIDI" in its name
foundPort = [name for name in mido.get_input_names() if 'loopMIDI' in name]
if len(foundPort) == 0:
    print("No loopMIDI port found. Please create one and try again.")
    quit()
else:  # Use the first port that has "loopMIDI" in its name
    foundPort = foundPort[0]


inport = mido.open_input(name=foundPort)

print("Listening for MIDI input...")

try:
    while True:
        msg_buffer = []
        for msg in inport.iter_pending():
            motor_index = msg.channel
            if motor_index > motor_channels - 1:
                continue
            if msg.type == 'note_on':
                frequency = note_to_frequency(msg.note)
                msg_buffer.append(
                    {'type': 'note_on', 'freq': frequency, 'channel': motor_index})
            elif msg.type == 'note_off':
                msg_buffer.append({'type': 'note_off', 'channel': motor_index})
        if len(msg_buffer) > 0:
            send_buffer_to_arduino(msg_buffer)

        # Check if it has been more than 5 seconds since the last MIDI activity
        if time.time() - last_midi_activity_time > 5:
            disable_motors()  # Disable motors after 5 seconds of inactivity


finally:
    inport.close()
    ser.close()
    print("Ports closed.")
