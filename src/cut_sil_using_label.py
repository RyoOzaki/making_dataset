import numpy as np
from pathlib import Path
from scipy.io import wavfile
from argparse import ArgumentParser

def load_label(file, parser):
    raw_lab = file.read_text().split("\n")
    raw_lab = [line for line in raw_lab if line]
    lab_parsed = [label_parser.parse_args(line.split(" ")) for line in raw_lab]
    lab = [[parsed.begin, parsed.end, parsed.lab] for parsed in lab_parsed]

    return lab

def convert_label_to_wave_frame(labels, fs):
    new_labels = [
        [int(bt*fs), int(et*fs)-1, lab]
        for (bt, et, lab) in labels
    ]
    new_labels[-1][1] += 1
    return new_labels

def minus_offset(labels, offset):
    new_labels = [
        [bf-offset, ef-offset, lab]
        for (bf, ef, lab) in labels
    ]
    new_labels[-1][1] += 1
    return new_labels

def convert_label_to_time(labels, fs):
    labels[-1][1] -= 1
    new_labels = [
        [bf / fs, (ef + 1) / fs, lab]
        for (bf, ef, lab) in labels
    ]
    return new_labels

parser = ArgumentParser()

parser.add_argument("--source_dir", type=Path, required=True)
parser.add_argument("--label_format", default="time", choices=["time", "wave_frame"])

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--replace", action="store_true")
group.add_argument("--output_dir", type=Path)

args = parser.parse_args()

for wav_file in args.source_dir.glob("**/*.wav"):
    fs, signal = wavfile.read(wav_file)

    phn_file = wav_file.with_suffix(".raw_phn")
    wrd_file = wav_file.with_suffix(".raw_wrd")

    label_parser = ArgumentParser()
    if args.label_format == "time":
        label_parser.add_argument("begin", type=float)
        label_parser.add_argument("end", type=float)
        label_parser.add_argument("lab", type=str)
    else:
        label_parser.add_argument("begin", type=int)
        label_parser.add_argument("end", type=int)
        label_parser.add_argument("lab", type=str)

    phn = load_label(phn_file, label_parser)
    wrd = load_label(wrd_file, label_parser)

    if args.label_format == "time":
        phn = convert_label_to_wave_frame(phn, fs)
        wrd = convert_label_to_wave_frame(wrd, fs)

    assert phn[0][2] in ["<s>", "</s>", "silB", "silE", "sil", "sp"]
    assert phn[-1][2] in ["<s>", "</s>", "silB", "silE", "sil", "sp"]
    assert wrd[0][2] in ["<s>", "</s>", "silB", "silE", "sil", "sp"]
    assert wrd[-1][2] in ["<s>", "</s>", "silB", "silE", "sil", "sp"]

    begin_frame = phn[1][0]
    end_frame = phn[-1][0]

    signal = signal[begin_frame:end_frame]
    phn = minus_offset(phn[1:-1], begin_frame)
    wrd = minus_offset(wrd[1:-1], begin_frame)

    if args.replace:
        out_wav_file = wav_file
    else:
        out_wav_file = args.output_dir / wav_file.relative_to(args.source_dir)
        out_wav_file.parent.mkdir(parents=True, exist_ok=True)
    out_phn_file = out_wav_file.with_suffix(".raw_phn")
    out_wrd_file = out_wav_file.with_suffix(".raw_wrd")

    wavfile.write(out_wav_file, fs, signal)
    if args.label_format == "time":
        phn = convert_label_to_time(phn, fs)
        wrd = convert_label_to_time(wrd, fs)
        out_phn_file.write_text("\n".join(map(lambda x: f"{x[0]:.7f} {x[1]:.7f} {x[2]}", phn)))
        out_wrd_file.write_text("\n".join(map(lambda x: f"{x[0]:.7f} {x[1]:.7f} {x[2]}", wrd)))
    else:
        out_phn_file.write_text("\n".join(map(lambda x: f"{x[0]} {x[1]} {x[2]}", phn)))
        out_wrd_file.write_text("\n".join(map(lambda x: f"{x[0]} {x[1]} {x[2]}", wrd)))
