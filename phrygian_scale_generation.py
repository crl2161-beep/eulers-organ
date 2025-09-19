def generate_phrygian_scale_from_pythagorean(pythagorean_scale, num_octaves=2):
    phrygian_intervals = [0, 1, 3, 5, 7, 8, 10]
    base_phrygian_scale = [pythagorean_scale[i % len(pythagorean_scale)] for i in phrygian_intervals]
    phrygian_scale = []
    for octave in range(num_octaves):
        multiplier = 2 ** octave
        phrygian_scale.extend([freq * multiplier for freq in base_phrygian_scale])
    return phrygian_scale
