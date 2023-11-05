import mido
import serial
import time

# Constants for the MIDI to frequency conversion
A4_KEY = 69
A4_FREQ = 440

# Replace with your Arduino's serial port and the correct baud rate
arduino_port = 'COM6'  # This is typical for Unix
baud_rate = 115200

# Open serial connection to Arduino
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(3)  # wait for serial connection to initialize
channel_outputting = [False, False]


def note_to_frequency(note):
    """Convert a MIDI note number to a frequency in Hertz."""
    freq = A4_FREQ * 2 ** ((note - A4_KEY) / 12)
    return freq


def send_frequency_to_arduino(motor, freq):
    if channel_outputting[msg.channel]:
        stop_note(msg.channel)
    """Send frequency data to the Arduino over serial."""
    data = f's,{motor},{freq}\n'.encode()
    ser.write(data)
    channel_outputting[msg.channel] = True


def stop_note(motor):
    """Send stop signal to Arduino over serial."""
    if channel_outputting[motor]:
        data = f'e,{motor}\n'.encode()
        ser.write(data)
        channel_outputting[motor] = False


# Available MIDI ports
print(mido.get_input_names())  # List all available input ports

# Open the MIDI input port (replace 'MIDI keyboard' with the actual name or use a port number)
inport = mido.open_input(name="loopMIDI Port 2")

print("Listening for MIDI input...")

try:
    for msg in inport:
        if msg.channel > 3:
            continue
        if msg.type == 'note_on':
            frequency = note_to_frequency(msg.note)
            print(f'Note ON: {msg.note} -> Frequency: {frequency} Hz')
            send_frequency_to_arduino(msg.channel, frequency)
        elif msg.type == 'note_off':
            print(f'Note OFF: {msg.note} -> Stop signal sent')
            stop_note(msg.channel)

finally:
    inport.close()
    ser.close()
    print("Ports closed.")
