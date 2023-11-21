import mido
import os


def split_notes_to_channels(midi_file, new_midi_file, max_channels=15):
    mid = mido.MidiFile(midi_file)
    new_mid = mido.MidiFile()

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)

        active_notes = [None] * max_channels
        catch_all_channel = max_channels - 1  # Reserve the last channel as catch-all
        time_elapsed = 0

        for msg in track:
            time_elapsed += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                channel = find_free_channel(
                    active_notes, time_elapsed, max_channels)
                if channel is None:
                    channel = catch_all_channel  # Redirect to catch-all channel if no free channel

                new_track.append(mido.Message(
                    'note_on', note=msg.note, velocity=msg.velocity, time=msg.time, channel=channel))
                end_time = time_elapsed + 480  # Adjust as needed
                active_notes[channel] = (msg.note, end_time)

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Look for the note in active channels first, then in the catch-all channel
                channel = next((i for i, v in enumerate(
                    active_notes) if v and v[0] == msg.note), catch_all_channel)
                new_track.append(mido.Message(
                    'note_off', note=msg.note, velocity=msg.velocity, time=msg.time, channel=channel))
                active_notes[channel] = None

            else:
                new_track.append(msg.copy())

            if msg.type in ['note_on', 'note_off']:
                time_elapsed = 0

    new_mid.save(new_midi_file)


def find_free_channel(active_notes, current_time, max_channels):
    # Exclude the catch-all channel
    for i, active_note in enumerate(active_notes[:-1]):
        if active_note is None or (active_note[1] <= current_time):
            return i

    # If all channels are busy and cannot exceed max_channels, return None
    return None


# Example usage code
current_path = os.getcwd()
for file in os.listdir(os.path.join(current_path, "Tools", "input")):
    if file.endswith(".mid"):
        input_path = os.path.join(current_path, "Tools", "input", file)
        output_path = os.path.join(current_path, "Tools", "output", file)
        # Set your desired number of channels here (max 16)
        split_notes_to_channels(input_path, output_path, max_channels=5)
