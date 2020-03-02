import numpy as np
from pathlib import Path
import re
import argparse
from utility.converts import convert_label_to_time, convert_label_to_wave_frame

def parse(body):
    word_label_pattern    = r"^\[\s+(?P<begin_frame>\d+)\s+(?P<end_frame>\d+)\].*\s+.*\s+\[(?P<word_unit>.*)\]$"
    phoneme_label_pattern = r"^\[\s+(?P<begin_frame>\d+)\s+(?P<end_frame>\d+)\].*\s+(?P<triphone_unit>.*)$"

    i = 1
    while "word alignment" not in body[i]:
        i += 1
    while not body[i].startswith("["):
        i += 1
    word_labels = []
    while body[i].startswith("["):
        m = re.search(word_label_pattern, body[i])
        bf = int(m.group("begin_frame"))
        ef = int(m.group("end_frame"))
        word_unit = m.group("word_unit")
        word = word_unit
        if "+" in word:
            word = word[:word.index("+")]

        word_labels.append((bf, ef, word))
        i += 1
    sentence = [w for (_, _, w) in word_labels]

    while "phoneme alignment" not in body[i]:
        i += 1
    while not body[i].startswith("["):
        i += 1
    phoneme_labels = []
    while body[i].startswith("["):
        # print("body: ", body[i])
        m = re.search(phoneme_label_pattern, body[i])
        bf = int(m.group("begin_frame"))
        ef = int(m.group("end_frame"))
        triphone_unit = m.group("triphone_unit")
        if "[" in triphone_unit:
            triphone_unit = triphone_unit[:triphone_unit.index("[")]
        phoneme = triphone_unit
        if "-" in phoneme:
            phoneme = phoneme[phoneme.index("-")+1:]
        if "+" in phoneme:
            phoneme = phoneme[:phoneme.index("+")]
        if "_" in phoneme:
            phoneme = phoneme[:phoneme.index("_")]

        phoneme_labels.append((bf, ef, phoneme))
        i += 1

    return sentence, phoneme_labels, word_labels

parser = argparse.ArgumentParser()

parser.add_argument("--source_dir", type=Path, default="./raw_wav", help="source dir")
parser.add_argument("--samplerate", type=int, default=48000, choices=[16000, 48000])
parser.add_argument("--label_format", default="time", choices=["time", "wave_frame", "mfcc_frame"])

args = parser.parse_args()

for jout_file in args.source_dir.glob("**/*.out"):
    body = jout_file.read_text().split("\n")
    snt, phn_lab, wrd_lab = parse(body)

    if args.label_format == "time":
        phn_lab = convert_label_to_time(phn_lab)
        wrd_lab = convert_label_to_time(wrd_lab)
    elif args.label_format == "wave_frame":
        phn_lab = convert_label_to_wave_frame(phn_lab, fs=args.samplerate)
        wrd_lab = convert_label_to_wave_frame(wrd_lab, fs=args.samplerate)

    output_file = jout_file.with_suffix(".raw_phn")
    if args.label_format == "time":
        output_file.write_text("\n".join(map(lambda x: f"{x[0]:.7f} {x[1]:.7f} {x[2]}", phn_lab)))
    else:
        output_file.write_text("\n".join(map(lambda x: f"{x[0]} {x[1]} {x[2]}", phn_lab)))

    output_file = jout_file.with_suffix(".raw_wrd")
    if args.label_format == "time":
        output_file.write_text("\n".join(map(lambda x: f"{x[0]:.7f} {x[1]:.7f} {x[2]}", wrd_lab)))
    else:
        output_file.write_text("\n".join(map(lambda x: f"{x[0]} {x[1]} {x[2]}", wrd_lab)))
