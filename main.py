import numpy as np
from waveform_analysis import (
    generate_sine_wave_euler,
    generate_sine_wave_with_harmonics,
    extract_fundamental_frequency
)
from scale_generation import generate_pythagorean_scale_from_frequency
from visualization import show_melody_lines, plot_waveform, plot_circle, plot_scale
from melody_generation import generate_phrygian_melody, generate_phrygian_rhythm
from melody_playback import synthesize_melody_with_harmonics, play_melody
from phrygian_scale_generation import generate_phrygian_scale_from_pythagorean

# ------------------------------------------------------------------------------------
def find_nearest_scale_tone(target_freq, scale):
    if isinstance(target_freq, np.ndarray):
        target_freq = target_freq.item()
    return min(scale, key=lambda x: abs(x - target_freq))

def generate_phrygian_triad(melody_freq, scale):
    minor_third_ratio = 2 ** (3/12)
    perfect_fifth_ratio = 2 ** (7/12)

    root_freq = find_nearest_scale_tone(melody_freq, scale)
    third_freq = find_nearest_scale_tone(root_freq * minor_third_ratio, scale)
    fifth_freq = find_nearest_scale_tone(root_freq * perfect_fifth_ratio, scale)

    return root_freq, third_freq, fifth_freq
# ------------------------------------------------------------------------------------

# Parameters
sample_rate = 44100
duration = 1.0
num_harmonics = 600
decay_factor = 10
num_notes = 16
rhythm_pattern = "repeating"   # repeating, random, sacred, epic, ancient_greek
melody_style = "melodic_arch"  # melodic_arch, call_response

# Step 1: Generate sine wave
print("Generating regular sine wave...")
t_values, sine_wave = generate_sine_wave_euler(sample_rate=sample_rate, duration=duration)
plot_waveform(t_values, sine_wave)
plot_circle(sine_wave)

# Step 2: Extract fundamental + generate harmonic sine
fundamental_frequency = extract_fundamental_frequency(sine_wave, sample_rate)
print(f"Extracted Fundamental Frequency: {fundamental_frequency:.2f} Hz")

print("Generating harmonic sine wave...")
t_values, harmonic_wave = generate_sine_wave_with_harmonics(
    frequency=fundamental_frequency,
    sample_rate=sample_rate,
    duration=duration,
    num_harmonics=num_harmonics,
    decay_factor=decay_factor
)
plot_waveform(t_values, harmonic_wave)
plot_circle(harmonic_wave)

# Step 3: Generate scales
pythagorean_scale = generate_pythagorean_scale_from_frequency(fundamental_frequency, octaves=2)
plot_scale(pythagorean_scale, title="Pythagorean Scale")

phrygian_scale = generate_phrygian_scale_from_pythagorean(pythagorean_scale, num_octaves=2)
phrygian_scale = sorted(phrygian_scale)

# Step 4: Rhythm + Melody (frequencies only)
rhythm = generate_phrygian_rhythm(num_notes=num_notes, rhythm_pattern=rhythm_pattern)
melody = generate_phrygian_melody(
    pythagorean_scale,
    num_notes=num_notes,
    melody_style=melody_style,
    rhythm=rhythm,
    sample_rate=sample_rate,
    duration=duration,
    num_harmonics=num_harmonics,
    decay_factor=decay_factor
)

# Step 5: Triads
triad_harmonies = [generate_phrygian_triad(note, phrygian_scale) for note in melody]
melody_line = [t[0] for t in triad_harmonies]
harmony_line_1 = [t[2] for t in triad_harmonies]
harmony_line_2 = [t[1] for t in triad_harmonies]

# Trim to rhythm length
min_len = min(len(melody_line), len(harmony_line_1), len(harmony_line_2), len(rhythm))
melody_line, harmony_line_1, harmony_line_2, rhythm = (
    melody_line[:min_len],
    harmony_line_1[:min_len],
    harmony_line_2[:min_len],
    rhythm[:min_len],
)

# Step 6: Display + plot
show_melody_lines(
    [melody_line, harmony_line_1, harmony_line_2],
    rhythm,
    labels=["Melody", "Fifth Harmony", "Third Harmony"]
)

# Step 7: Synthesis
melody_waveform = synthesize_melody_with_harmonics(melody_line, rhythm, sample_rate, num_harmonics, decay_factor)
harmony_waveform = synthesize_melody_with_harmonics(harmony_line_1, rhythm, sample_rate, num_harmonics, decay_factor)
third_harmony_waveform = synthesize_melody_with_harmonics(harmony_line_2, rhythm, sample_rate, num_harmonics, decay_factor)

# Volume balance
melody_waveform *= 0.90
harmony_waveform *= 0.60
third_harmony_waveform *= 0.80

# Align lengths
min_len = min(len(melody_waveform), len(harmony_waveform), len(third_harmony_waveform))
melody_waveform = melody_waveform[:min_len]
harmony_waveform = harmony_waveform[:min_len]
third_harmony_waveform = third_harmony_waveform[:min_len]

# Combine & normalize
combined_waveform = melody_waveform + harmony_waveform + third_harmony_waveform
max_amp = np.max(np.abs(combined_waveform))
if max_amp > 0:
    combined_waveform = 0.95 * combined_waveform / max_amp

# Step 8: Play
print("Playing combined melody...")
play_melody(combined_waveform, sample_rate)
