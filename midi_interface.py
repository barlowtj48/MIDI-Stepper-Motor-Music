import mido
import serial
import time
import re

# Constants for the MIDI to frequency conversion
A4_KEY = 69
A4_FREQ = 432

# Replace with your Arduino's serial port and the correct baud rate
# TODO: support command line arguments for port
arduino_port = 'COM6'

baud_rate = 115200
motor_channels = 0

# Open serial connection to Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
except:
    print("Serial connection failed. Please check your port and baud rate and try again.")
    quit()
time.sleep(3)  # wait for serial connection to initialize
# Read from the serial to determine how many motors are connected
start_time = time.time()
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
        print("Serial read failed. Please check your port and baud rate and try again.")
        quit()

# Keeps track of which channels are outputting
channel_outputting = [False] * motor_channels

last_midi_activity_time = time.time()
motors_enabled = True  # The motors are enabled by default


def note_to_frequency(note):
    """Convert a MIDI note number to a frequency in Hertz."""
    freq = A4_FREQ * 2 ** ((note - A4_KEY) / 12)
    return freq


def send_frequency_to_arduino(motor, freq):
    global last_midi_activity_time, motors_enabled
    last_midi_activity_time = time.time()
    motors_enabled = True
    if msg.channel > motor_channels - 1:
        return
    if channel_outputting[msg.channel]:
        stop_note(msg.channel)
    """Send frequency data to the Arduino over serial."""
    data = f's,{motor},{freq}\n'.encode()
    try:
        ser.write(data)
    except:
        print("Serial Write Failure. Was the device unplugged?")
        quit()
    channel_outputting[msg.channel] = True


def stop_note(motor):
    global last_midi_activity_time, motors_enabled
    last_midi_activity_time = time.time()
    motors_enabled = True
    """Send stop signal to Arduino over serial."""
    if msg.channel > motor_channels - 1:
        return
    if channel_outputting[motor]:
        data = f'e,{motor}\n'.encode()
        try:
            ser.write(data)
        except:
            print("Serial Write Failure. Was the device unplugged?")
            quit()
        channel_outputting[motor] = False


def disable_motors():
    """Send stop signal to all motors."""
    global motors_enabled
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
        for msg in inport.iter_pending():
            if msg.channel > motor_channels - 1:
                continue
            if msg.type == 'note_on':
                frequency = note_to_frequency(msg.note)
                print(f'Note ON: {msg.note} -> Frequency: {frequency} Hz')
                send_frequency_to_arduino(msg.channel, frequency)
            elif msg.type == 'note_off':
                print(f'Note OFF: {msg.note} -> Stop signal sent')
                stop_note(msg.channel)

        # Check if it has been more than 5 seconds since the last MIDI activity
        if time.time() - last_midi_activity_time > 5:
            disable_motors()  # Disable motors after 5 seconds of inactivity


finally:
    inport.close()
    ser.close()
    print("Ports closed.")
