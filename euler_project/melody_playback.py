import numpy as np
import sounddevice as sd
import soundfile as sf
from waveform_analysis import generate_sine_wave_with_harmonics

def synthesize_melody_with_harmonics(melody, rhythm, sample_rate, num_harmonics, decay_factor):
    waveform = np.array([], dtype=np.float32)
    for frequency, duration in zip(melody, rhythm):
        t, note_waveform = generate_sine_wave_with_harmonics(
            frequency=frequency,
            sample_rate=sample_rate,
            duration=duration,
            num_harmonics=num_harmonics,
            decay_factor=decay_factor
        )
        waveform = np.concatenate((waveform, note_waveform))
    return waveform

def play_melody(waveform, sample_rate):
    print("Playing melody...")
    sd.play(waveform, samplerate=sample_rate)
    sd.wait()

def save_melody_to_file(waveform, sample_rate, filename):
    waveform = np.asarray(waveform, dtype=np.float32)
    sf.write(filename, waveform, sample_rate)
    print(f"Saved melody to {filename}")
