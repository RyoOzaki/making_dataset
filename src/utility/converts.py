
def convert_label_to_time(labels):
    offset_align = 25E-3 / 2
    step = 10E-3
    new_labels = []

    (bf, ef, lab) = labels[0]
    new_labels.append([
        bf * step,
        (ef + 1) * step + offset_align,
        lab
    ])
    for (bf, ef, lab) in labels[1:]:
        new_labels.append([
            bf * step + offset_align,
            (ef + 1) * step + offset_align,
            lab
        ])
    return new_labels

def convert_label_to_wave_frame(labels, fs):
    # left include right exclude but final raw include left and right
    labels = convert_label_to_time(labels)
    new_labels = [
        [int(bt*fs), int(et*fs)-1, lab]
        for (bt, et, lab) in labels
    ]
    new_labels[-1][1] += 1
    return new_labels
