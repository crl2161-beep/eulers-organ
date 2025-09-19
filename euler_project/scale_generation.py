def pythagorean_ratios():
    return [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]

def generate_pythagorean_scale_from_frequency(base_frequency, octaves=1):
    ratios = pythagorean_ratios()
    scale = []
    for octave in range(octaves):
        for ratio in ratios:
            scale.append(base_frequency * ratio * (2 ** octave))
    return scale
