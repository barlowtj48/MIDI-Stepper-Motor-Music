import mido
import serial
import time

# Constants for the MIDI to frequency conversion
A4_KEY = 69
A4_FREQ = 432

# Replace with your Arduino's serial port and the correct baud rate
arduino_port = 'COM6'  # This is typical for Unix
baud_rate = 115200

# Open serial connection to Arduino
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(3)  # wait for serial connection to initialize
channel_outputting = [False, False, False, False]

last_midi_activity_time = time.time()
motors_enabled = True


def note_to_frequency(note):
    """Convert a MIDI note number to a frequency in Hertz."""
    freq = A4_FREQ * 2 ** ((note - A4_KEY) / 12)
    return freq


def send_frequency_to_arduino(motor, freq):
    global last_midi_activity_time, motors_enabled
    last_midi_activity_time = time.time()
    motors_enabled = True
    if msg.channel > 3:
        return
    if channel_outputting[msg.channel]:
        stop_note(msg.channel)
    """Send frequency data to the Arduino over serial."""
    data = f's,{motor},{freq}\n'.encode()
    try:
        ser.write(data)
    except:
        print("Serial write failed")
        quit()
    channel_outputting[msg.channel] = True


def stop_note(motor):
    global last_midi_activity_time, motors_enabled
    last_midi_activity_time = time.time()
    motors_enabled = True
    """Send stop signal to Arduino over serial."""
    if msg.channel > 3:
        return
    if channel_outputting[motor]:
        data = f'e,{motor}\n'.encode()
        try:
            ser.write(data)
        except:
            print("Serial write failed")
            quit()
        channel_outputting[motor] = False


def disable_motors():
    """Send stop signal to all motors."""
    global motors_enabled
    if not motors_enabled:
        return
    print("Disabling motors.")
    motors_enabled = False
    data = b'd\n'
    try:
        ser.write(data)
    except:
        print("Serial write failed")
        quit()


# Available MIDI ports
print(mido.get_input_names())  # List all available input ports

# Find the port that has "loopMIDI" in its name
foundPort = [name for name in mido.get_input_names() if 'loopMIDI' in name]
if len(foundPort) == 0:
    print("No loopMIDI port found. Please create one and try again.")
    exit(1)
else:  # Use the first port that has "loopMIDI" in its name
    foundPort = foundPort[0]


# Open the MIDI input port (replace 'MIDI keyboard' with the actual name or use a port number)
inport = mido.open_input(name=foundPort)

print("Listening for MIDI input...")

try:
    while True:
        for msg in inport.iter_pending():
            if msg.channel > 3:
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
