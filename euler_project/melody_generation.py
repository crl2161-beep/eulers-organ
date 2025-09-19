import random

def generate_phrygian_melody(
    pythagorean_scale,
    num_notes,
    melody_style,
    rhythm,
    sample_rate,
    duration,
    num_harmonics,
    decay_factor
):
    melody = []
    current_note = pythagorean_scale[0]
    peak_reached = False
    tonic_reached = False
    alternate_direction = False

    for i in range(num_notes):
        if melody_style == "melodic_arch":
            if peak_reached:
                interval_choice = random.choice([1, 2, 3])
                next_note_index = max(pythagorean_scale.index(current_note) - interval_choice, 0)
            else:
                interval_choice = random.choice([1, 2, 3])
                next_note_index = min(pythagorean_scale.index(current_note) + interval_choice,
                                      len(pythagorean_scale) - 1)
                if current_note == pythagorean_scale[-1]:
                    peak_reached = True
            current_note = pythagorean_scale[next_note_index]
            melody.append(current_note)

        elif melody_style == "call_response":
            if i % 8 == 0:
                current_note = pythagorean_scale[0]
                tonic_reached = True
            else:
                if tonic_reached:
                    if alternate_direction:
                        interval_choice = random.choice([2, 3, 4])
                        next_note_index = min(pythagorean_scale.index(current_note) + interval_choice,
                                              len(pythagorean_scale) - 1)
                        alternate_direction = False
                    else:
                        interval_choice = random.choice([1, 2])
                        next_note_index = max(pythagorean_scale.index(current_note) - interval_choice, 0)
                        alternate_direction = True
                    current_note = pythagorean_scale[next_note_index]
                else:
                    direction = random.choice(['up', 'down'])
                    interval_choice = random.choice([1, 2])
                    if direction == 'up':
                        next_note_index = min(pythagorean_scale.index(current_note) + interval_choice,
                                              len(pythagorean_scale) - 1)
                    else:
                        next_note_index = max(pythagorean_scale.index(current_note) - interval_choice, 0)
                    current_note = pythagorean_scale[next_note_index]
            melody.append(current_note)

    return melody

def generate_phrygian_rhythm(num_notes, rhythm_pattern="epic"):
    rhythm = []

    if rhythm_pattern == "repeating":
        motif = [0.5, 0.25, 0.75, 1.0]
        rhythm = motif * (num_notes // len(motif)) + motif[:num_notes % len(motif)]
    elif rhythm_pattern == "random":
        rhythm = [random.uniform(0.25, 1.0) for _ in range(num_notes)]
    elif rhythm_pattern == "sacred":
        for i in range(num_notes):
            rhythm.append(1.5 if (i + 1) % 4 == 0 else 0.5)
    elif rhythm_pattern == "epic":
        layer1 = [0.5, 0.25, 0.75, 1.5]
        layer2 = [0.25, 0.75, 0.5, 1.0]
        layer1 = layer1 * (num_notes // len(layer1)) + layer1[:num_notes % len(layer1)]
        layer2 = layer2 * (num_notes // len(layer2)) + layer2[:num_notes % len(layer2)]
        rhythm = [min(layer1[i], layer2[i]) for i in range(num_notes)]
    elif rhythm_pattern == "ancient_greek":
        while len(rhythm) < num_notes:
            if len(rhythm) % 4 == 0:
                rhythm.append(random.uniform(1.5, 2.0))
            else:
                if random.choice([True, False]):
                    rhythm.append(random.choice([0.5, 1.0, 1.25]))
                else:
                    rhythm.append(random.choice([1.0, 1.25, 1.5]))
            if len(rhythm) == num_notes:
                break

    # Normalize rhythm to ~10s total
    total_duration = sum(rhythm)
    scale_factor = 10.0 / total_duration
    rhythm = [d * scale_factor for d in rhythm]

    return rhythm
