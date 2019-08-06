import numpy as np
from pathlib import Path
from itertools import product
from argparse import ArgumentParser
from configparser import ConfigParser
from math import sqrt
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def load_word_dict(file, delimiter):
    body = file.read_text().split("\n")
    body = [b for b in body if b and not b.startswith("#")]
    body = [b.split(delimiter) for b in body]
    body = [[wrd.strip(), [phn.strip() for phn in phns.split(" ") if phn]] for wrd, phns in body]
    return {wrd: phns for wrd, phns in body}

def load_sentences(file):
    body = file.read_text().split("\n")
    body = [b for b in body if b and not b.startswith("#")]
    return [[wrd.strip() for wrd in snt.split(" ") if wrd] for snt in body if snt]

wdict_ext = "wdict"

parser = ArgumentParser()
parser.add_argument("source_file", type=Path, help="source file of dataset")

parser.add_argument("-o", "--output_dir", type=Path, default="./synthetic_data", help="dir of saving summary files and figures")

parser.add_argument("--delimiter", type=str, default=":=", help="delimiter of word dictionary")
parser.add_argument("--repeat", type=int, default=1, help="repeat count of sentence in source file")

args = parser.parse_args()

source_file = args.source_file
source_dir = source_file.parent
output_dir = args.output_dir
target_name = source_file.stem

delimiter = args.delimiter
repeat = args.repeat

output_dir.mkdir(exist_ok=True)

wdict_file = source_dir / f"{target_name}.{wdict_ext}"

word_dict = load_word_dict(wdict_file, delimiter)
sentences = load_sentences(source_file) * repeat
wrd_list = list(set(word_dict.keys()))
wrd_list.sort()
phn_list = list(set([phn for phns in word_dict.values() for phn in phns]))
phn_list.sort()

wrd_N = len(wrd_list)
phn_N = len(phn_list)

M = int(np.ceil((np.sqrt(phn_N + 1) - 1) / 2))
tmp = np.zeros(M * 2 + 1)
tmp[1::2] = np.arange(1, M+1)
tmp[2::2] = -np.arange(1, M+1)

points = list(product(tmp, repeat=2))[1:]
points.sort(key=lambda x: sqrt(x[0]**2 + x[1]**2))
coval_var = 0.001
covariance = np.identity(2) * coval_var

if repeat <= 1:
    repeat = 1
    filename_fmt = r"{snt_txt}"
else:
    filename_fmt = r"{snt_txt}_{rep_idx}"
output_dir.mkdir(exist_ok=True)
output_target_dir = output_dir / f"{target_name}"
output_target_dir.mkdir(exist_ok=True)

for idx in range(repeat):
    for sentence in sentences:
        phn_sentence = []
        wrd_sentence = []
        for word in sentence:
            phn_sentence.extend([phn_list.index(p) for p in word_dict[word]])
            wrd_sentence.extend([wrd_list.index(word)] * len(word_dict[word]))
        phn_sentence = np.array(phn_sentence, dtype=int)
        wrd_sentence = np.array(wrd_sentence, dtype=int)
        dat_sentence = np.zeros((phn_sentence.shape[0], 2))
        for phn_idx, mean in zip(range(phn_N), points):
            flag = (phn_sentence == phn_idx)
            if np.any(flag):
                dat_sentence[flag] = multivariate_normal.rvs(mean=mean, cov=covariance, size=flag.sum())
        fstem = filename_fmt.format(snt_txt="_".join(sentence), rep_idx=idx+1)
        DATA_dir = output_target_dir / "DATA"
        DATA_dir.mkdir(exist_ok=True)
        LABEL_dir = output_target_dir / "LABEL"
        LABEL_dir.mkdir(exist_ok=True)
        np.savetxt(DATA_dir / f"{fstem}.txt", dat_sentence)
        np.savetxt(LABEL_dir / f"{fstem}.lab", phn_sentence, fmt="%d")
        np.savetxt(LABEL_dir / f"{fstem}.lab2", wrd_sentence, fmt="%d")

#%% making parameters config file
config_parser = ConfigParser()

for i, mean in zip(range(phn_N), points):
    sec_name = f"{i+1}_th"
    config_parser.add_section(sec_name)
    config_parser[sec_name]["mu"] = f"numpy.array([{mean[0]}, {mean[1]}])"
    config_parser[sec_name]["sigma"] = f"numpy.identity(2) * {coval_var}"
config_file = output_target_dir / "letter_observation.config"
with config_file.open("w") as f:
    config_parser.write(f)
