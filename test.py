import numpy as np
import sounddevice as sd

# Constants
SAMPLE_RATE = 44100  # Sample rate in Hertz
DURATION = 1  # Duration of the sound in seconds


def play_frequency(freq, duration=DURATION, sample_rate=SAMPLE_RATE):
    """
    Play a sound of the given frequency.

    :param freq: Frequency of the sound in Hertz
    :param duration: Duration of the sound in seconds
    :param sample_rate: Sample rate in Hertz
    """
    t = np.linspace(0, duration, int(
        sample_rate * duration), False)  # Time axis
    wave = 0.5 * np.sin(2 * np.pi * freq * t)  # Generate sine wave
    sd.play(wave, samplerate=sample_rate)  # Play audio
    sd.wait()  # Wait until playback is finished


# Example of playing back a frequency
play_frequency(560, 5)  # This will play a 440 Hz (A4) tone for 1 second
