import matplotlib.pyplot as plt
import numpy as np

def plot_waveform(t_values, waveform, downsample_factor=100):
    t_values = t_values[::downsample_factor]
    waveform = waveform[::downsample_factor]
    plt.figure(figsize=(10, 4))
    plt.plot(t_values, waveform, color="orange")
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

def plot_circle(waveform):
    waveform = waveform / np.max(np.abs(waveform))
    cos_vals = np.cos(2 * np.pi * waveform)
    sin_vals = np.sin(2 * np.pi * waveform)
    plt.figure(figsize=(6, 6))
    plt.plot(cos_vals, sin_vals, color="blue")
    plt.title("Circular Mapping")
    plt.axis("equal")
    plt.grid()
    plt.show()

def plot_scale(scale, title="Generated Scale"):
    plt.figure(figsize=(10, 4))
    plt.stem(scale, linefmt='r-', markerfmt='ro', basefmt=" ")
    plt.title(title)
    plt.xlabel("Note Index")
    plt.ylabel("Frequency (Hz)")
    plt.grid()
    plt.show()

def show_melody_lines(melodies, rhythm, labels=None, title="Melodies Over Time"):
    min_len = min(len(line) for line in melodies)
    min_len = min(min_len, len(rhythm))
    melodies = [line[:min_len] for line in melodies]
    rhythm = rhythm[:min_len]

    if labels is None:
        labels = [f"Line {i+1}" for i in range(len(melodies))]

    # Console output
    print("Generated Melody and Harmonies:")
    print("-------------------------------------")
    for i in range(min_len):
        row = [f"{labels[j]} = {float(melodies[j][i]):.2f} Hz" for j in range(len(melodies))]
        dur = f"Duration = {float(rhythm[i]):.2f} s"
        print(f"Note {i+1}: " + ", ".join(row) + f", {dur}")
    print("-------------------------------------")
    print(f"Total Notes: {min_len}")

    # Plot
    time_points = [0]
    for dur in rhythm:
        time_points.append(time_points[-1] + dur)
    mid_times = [(time_points[i] + time_points[i+1]) / 2 for i in range(len(rhythm))]

    plt.figure(figsize=(10, 6))
    for idx, melody in enumerate(melodies):
        plt.plot(mid_times, melody, marker='o', label=labels[idx])
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.grid(True)
    plt.legend()
    plt.show()
