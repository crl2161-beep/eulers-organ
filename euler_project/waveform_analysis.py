import numpy as np
import random
from scipy.fft import fft, fftfreq

def generate_sine_wave_euler(sample_rate, duration, min_freq=20, max_freq=100):
    # Randomize frequency range each time
    min_freq = random.uniform(10, 50)  # Random min frequency
    max_freq = random.uniform(60, 200)  # Random max frequency
    
    time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = min_freq + (max_freq - min_freq) * (np.sin(2 * np.pi * 0.05 * time) + 1) / 2  # Smooth transition
    dt = 1 / sample_rate
    instantaneous_phase = 2 * np.pi * np.cumsum(frequency) * dt
    complex_exponential = np.exp(1j * instantaneous_phase)
    sine_wave = np.imag(complex_exponential)
    
    return time, sine_wave  

def extract_fundamental_frequency(waveform, sample_rate):
    """
    Extract the fundamental frequency from a waveform using FFT.

    Args:
        waveform (numpy.ndarray): The waveform to analyze.
        sample_rate (int): The sampling rate in Hz.

    Returns:
        fundamental_frequency (float): The dominant frequency in Hz.
    """
    N = len(waveform)
    fft_values = fft(waveform)
    fft_magnitudes = np.abs(fft_values)

    # Generate frequency bins
    frequencies = fftfreq(N, d=1/sample_rate)

    # Keep only positive frequencies
    positive_frequencies = frequencies[frequencies > 0]
    positive_magnitudes = fft_magnitudes[frequencies > 0]

    # Find the fundamental frequency (the peak of the FFT magnitudes)
    fundamental_index = np.argmax(positive_magnitudes)
    fundamental_frequency = positive_frequencies[fundamental_index]

    return fundamental_frequency

def generate_sine_wave_with_harmonics(
    frequency,
    sample_rate,
    duration,
    num_harmonics,
    decay_factor,
    randomize=False
):
    """
    Generate a sine wave with harmonics.

    Args:
        frequency (float): Fundamental frequency in Hz.
        sample_rate (int): Samples per second.
        duration (float): Duration of waveform in seconds.
        num_harmonics (int): Number of harmonics to add.
        decay_factor (float): Decay rate of harmonics.
        randomize (bool): If True, override num_harmonics and decay_factor with random values.

    Returns:
        t (numpy.ndarray): Time array.
        composite_wave (numpy.ndarray): Composite waveform with harmonics.
    """
    import random
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # If randomize is enabled, override settings
    if randomize:
        num_harmonics = random.randint(3, 10)
        decay_factor = random.uniform(0.1, 1.5)

    composite_wave = np.sin(2 * np.pi * frequency * t)

    for n in range(2, num_harmonics + 1):
        harmonic_freq = n * frequency
        harmonic_wave = np.sin(2 * np.pi * harmonic_freq * t)
        harmonic_amplitude = 1 / (n ** decay_factor)
        composite_wave += harmonic_amplitude * harmonic_wave

    return t, composite_wave


def generate_harmony(base_melody, interval_ratio_1, octave_shift):
    """
    Generate a harmony for the melody based on an interval ratio and octave shift.

    Args:
        base_melody (list): List of frequencies in the original melody.
        interval_ratio (float): The ratio for the interval (e.g., perfect fifth).
        octave_shift (int): Number of octaves to shift the harmony.

    Returns:
        harmony_melody (list): List of frequencies representing the harmony.
    """
    harmony_melody = []
    for freq in base_melody:
        interval_freq = freq * interval_ratio_1
        shifted_freq = interval_freq * (2 ** octave_shift)
        harmony_melody.append(shifted_freq)
    return harmony_melody



def generate_third_harmony(base_melody, interval_ratio1, interval_ratio2, octave_shift):
    """
    Generate a third harmony for the melody that's musically in between the other two harmonies.
    The third harmony is calculated based on the provided interval ratios.

    Args:
        base_melody (list): List of frequencies in the original melody.
        interval_ratio1 (float): The ratio for the first interval (e.g., perfect fifth).
        interval_ratio2 (float): The ratio for the second interval (e.g., a major third).
        octave_shift (int): Number of octaves to shift the harmony.

    Returns:
        third_harmony_melody (list): List of frequencies representing the third harmony.
    """
    third_harmony_melody = []
    for freq in base_melody:
        # Calculate the first and second harmonies using the provided interval ratios
        first_harmony_freq = freq * interval_ratio1
        second_harmony_freq = freq * interval_ratio2

        # Calculate the third harmony based on the geometric mean of the first and second harmonies
        third_harmony_freq = np.sqrt(first_harmony_freq * second_harmony_freq)

        # Apply octave shift
        shifted_freq = third_harmony_freq * (2 ** octave_shift)
        third_harmony_melody.append(shifted_freq)
        
    return third_harmony_melody


