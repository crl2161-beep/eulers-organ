# Infinite Melody Generator

This project generates rich, polyphonic organ-like melodies using sine waves derived from Euler’s formula:

\[
e^{i\theta} = \cos(\theta) + i \sin(\theta)
\]

## Features

- Euler-based sine wave generation (pure or frequency-swept seed tones)  
- Fundamental extraction: via FFT  
- Scale construction:
  - Pythagorean scale from extracted fundamental  
  - Phrygian mode derived from it  
- Random melody generation with different rhythmic patterns:
  - `repeating`, `random`, `sacred`, `epic`, `ancient_greek`  
- Triadic harmonization (root, third, fifth)  
- Additive synthesis with hundreds of harmonics → bright, organ-like sound  
- Visualization:
  - Waveforms  
  - Circular mappings  
  - Scale plots  
  - Melody + harmony lines  
- Playback & export:
  - Real-time audio (via `sounddevice`)  
  - Save as `.wav` (via `soundfile`)  

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
