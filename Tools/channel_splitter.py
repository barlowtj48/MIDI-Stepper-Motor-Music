import mido
from collections import defaultdict
import os


def split_notes_to_channels(midi_file, new_midi_file):
    mid = mido.MidiFile(midi_file)
    new_mid = mido.MidiFile()

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)

        # Track (note, time_since_last_event, total_time_elapsed) for each channel
        active_notes = [None] * 16
        time_elapsed = 0

        for msg in track:
            time_elapsed += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                channel = find_free_channel(active_notes, time_elapsed)
                new_track.append(mido.Message(
                    'note_on', note=msg.note, velocity=msg.velocity, time=msg.time, channel=channel))
                active_notes[channel] = (msg.note, msg.time, time_elapsed)

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                channel = next((i for i, v in enumerate(
                    active_notes) if v and v[0] == msg.note), None)
                if channel is not None:
                    new_track.append(mido.Message(
                        'note_off', note=msg.note, velocity=msg.velocity, time=msg.time, channel=channel))
                    active_notes[channel] = None

            else:
                new_track.append(msg.copy())

            # Adjust the time_elapsed for the next event
            if msg.type in ['note_on', 'note_off']:
                time_elapsed = 0

    new_mid.save(new_midi_file)


def find_free_channel(active_notes, current_time):
    for i, active_note in enumerate(active_notes):
        if active_note is None or (active_note[2] + active_note[1] <= current_time):
            return i

    # Use the channel with the earliest ending note
    return min(enumerate(active_notes), key=lambda x: (x[1][2] + x[1][1] if x[1] else float('inf')))[0]


# Example usage code
current_path = os.getcwd()
for file in os.listdir(os.path.join(current_path, "Tools", "input")):
    if file.endswith(".mid"):
        input_path = os.path.join(current_path, "Tools", "input", file)
        output_path = os.path.join(current_path, "Tools", "output", file)
        split_notes_to_channels(input_path, output_path)
