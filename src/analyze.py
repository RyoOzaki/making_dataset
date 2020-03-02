import numpy as np
from pathlib import Path
from itertools import product
import matplotlib.pyplot as plt
import japanize_matplotlib
from argparse import ArgumentParser
from utility.loads import load_word_dict, load_sentences, load_stems

wdict_ext = "wdict"

parser = ArgumentParser()
parser.add_argument("source_file", type=Path, help="source file of dataset")

parser.add_argument("-o", "--output_dir", type=Path, default="./analyze_summary", help="dir of saving summary files and figures")

parser.add_argument("--figure_ext", type=str, default="png", help="extension of figure")
parser.add_argument("--delimiter", type=str, default=":=", help="delimiter of word dictionary")
parser.add_argument("--repeat", type=int, default=1, help="repeat count of sentence in source file")
parser.add_argument("--pfsize", type=int, default=10, help="font size in figure of phoneme bigram")
parser.add_argument("--wfsize", type=int, default=10, help="font size in figure of word bigram")
parser.add_argument("--fcolor", type=str, default="black", help="font color in figure of bigram")
parser.add_argument("--cmap", type=str, default="rainbow", help="color map in figure of bigram")

args = parser.parse_args()
source_file = args.source_file
source_dir = source_file.parent
output_dir = args.output_dir
target_name = source_file.stem

figure_ext = args.figure_ext
delimiter = args.delimiter
repeat = args.repeat
pfsize = args.pfsize
wfsize = args.wfsize
fcolor = args.fcolor
cmap = args.cmap

wdict_file = source_dir / f"{target_name}.{wdict_ext}"

word_dict = load_word_dict(wdict_file, delimiter)
sentences = load_sentences(source_file) * repeat
wrd_list = list(set(word_dict.keys()))
wrd_list.sort()
phn_list = list(set([phn for phns in word_dict.values() for phn in phns]))
phn_list.sort()

output_dir.mkdir(exist_ok=True)
output_target_dir = output_dir / f"{target_name}"
output_target_dir.mkdir(exist_ok=True)

#%% Saving summary file
output_summary = output_target_dir / "Summary.txt"
with output_summary.open("w") as f:
    print(f"Sentence_N: {len(sentences)}", file=f)
    print(f"Unique word N: {len(wrd_list)}", file=f)
    print(f"Unique phoneme N: {len(phn_list)}", file=f)
    print(f"", file=f)
    print(f"Total word N: {sum([len(snt) for snt in sentences])}", file=f)
    print(f"Total phoneme N: {sum([len(word_dict[wrd]) for snt in sentences for wrd in snt])}", file=f)
    print(f"Mean of words per sentence: {sum([len(snt) for snt in sentences]) / len(sentences)}", file=f)
    print(f"Mean of phonemes per sentence: {sum([len(word_dict[wrd]) for snt in sentences for wrd in snt]) / len(sentences)}", file=f)
    print(f"", file=f)
    print(f"Max number of words in a sentence: {max([len(snt) for snt in sentences])}", file=f)
    print(f"Max number of phonemes in a sentence: {max([sum([len(word_dict[wrd]) for wrd in snt]) for snt in sentences])}", file=f)
    print(f"Min number of words in a sentence: {min([len(snt) for snt in sentences])}", file=f)
    print(f"Min number of phonemes in a sentence: {min([sum([len(word_dict[wrd]) for wrd in snt]) for snt in sentences])}", file=f)

output_file = output_target_dir / "Word_list.txt"
output_file.write_text("\n".join(wrd_list))

output_file = output_target_dir / "Phoneme_list.txt"
output_file.write_text("\n".join(phn_list))

#%% Initialize figure object of matplotlib
plt.figure(figsize=(10, 8))

#%% Word rank
word_N = len(wrd_list)
count = np.zeros(word_N, dtype=int)
for snt in sentences:
    for wrd in snt:
        count[wrd_list.index(wrd)] += 1
args = np.argsort(count)[::-1]
x = range(word_N)

output_file = output_target_dir / "Word_ranking.npz"
np.savez(output_file, word_list=np.array(wrd_list), count=count)

plt.clf()
plt.bar(x, count[args])
plt.xticks(x, np.array(wrd_list)[args], rotation=90)
plt.title("Word ranking")
plt.savefig(output_target_dir / f"Word_ranking.{figure_ext}")

#%% Phoneme rank
phoneme_N = len(phn_list)
count = np.zeros(phoneme_N, dtype=int)
for snt in sentences:
    for wrd in snt:
        for phn in word_dict[wrd]:
            count[phn_list.index(phn)] += 1
args = np.argsort(count)[::-1]
x = range(phoneme_N)

output_file = output_target_dir / "Phoneme_ranking.npz"
np.savez(output_file, phoneme_list=np.array(phn_list), count=count)

plt.clf()
plt.bar(x, count[args])
plt.xticks(x, np.array(phn_list)[args], rotation=90)
plt.title("Phoneme ranking")
plt.savefig(output_target_dir / f"Phoneme_ranking.{figure_ext}")

#%% Word dictionary
word_N = len(wrd_list)
phoneme_N = len(phn_list)
count = np.zeros((word_N, phoneme_N), dtype=int)
for wrd_idx, wrd in enumerate(wrd_list):
    for phn in word_dict[wrd]:
        phn_idx = phn_list.index(phn)
        count[wrd_idx, phn_idx] += 1

x = np.arange(phoneme_N) + 0.5
y = np.arange(word_N) + 0.5


output_file = output_target_dir / "Word_dictionary.npz"
np.savez(output_file, word_list=np.array(wrd_list), phoneme_list=np.array(phn_list), count=count)

plt.clf()
plt.pcolor(count[::-1], cmap=cmap)
plt.yticks(y, wrd_list[::-1])
plt.xticks(x, phn_list, rotation=90)
for i, j in product(range(word_N), range(phoneme_N)):
    if count[i, j] != 0:
        plt.text(x[j], y[::-1][i], count[i, j], size=pfsize, color=fcolor, verticalalignment="center", horizontalalignment="center")
plt.ylabel("Word")
plt.xlabel("Phoneme")
plt.title("Word dictionary (Bag of phonemes)")
plt.savefig(output_target_dir / f"Word_dictionary.{figure_ext}")

#%% Preprocess for making bigram
wrd_list = ["<s>", *wrd_list, "</s>"]
phn_list = ["<s>", *phn_list, "</s>"]

#%% Word bigram
word_N = len(wrd_list)
count = np.zeros((word_N, word_N), dtype=int)
for snt in sentences:
    snt = ["<s>", *snt, "</s>"]
    for from_wrd, to_wrd in zip(snt[:-1], snt[1:]):
        from_idx = wrd_list.index(from_wrd)
        to_idx = wrd_list.index(to_wrd)
        count[from_idx, to_idx] += 1
x = np.arange(word_N) + 0.5

output_file = output_target_dir / "Word_bigram.npz"
np.savez(output_file, word_list=np.array(wrd_list), count=count)

plt.clf()
plt.pcolor(count[::-1], cmap=cmap)
plt.yticks(x, wrd_list[::-1])
plt.xticks(x, wrd_list, rotation=90)
for i, j in product(range(word_N), repeat=2):
    if count[i, j] != 0:
        plt.text(x[j], x[::-1][i], count[i, j], size=wfsize, color=fcolor, verticalalignment="center", horizontalalignment="center")
plt.ylabel("From word")
plt.xlabel("To word")
plt.title("Word bigram")
plt.savefig(output_target_dir / f"Word_bigram.{figure_ext}")

#%% Phoneme bigram
phoneme_N = len(phn_list)
count = np.zeros((phoneme_N, phoneme_N), dtype=int)
for snt in sentences:
    phn_snt = []
    for wrd in snt:
        phn_snt.extend(word_dict[wrd])
    phn_snt = ["<s>", *phn_snt, "</s>"]
    for from_wrd, to_wrd in zip(phn_snt[:-1], phn_snt[1:]):
        from_idx = phn_list.index(from_wrd)
        to_idx = phn_list.index(to_wrd)
        count[from_idx, to_idx] += 1
x = np.arange(phoneme_N) + 0.5

output_file = output_target_dir / "Phoneme_bigram.npz"
np.savez(output_file, phoneme_list=np.array(phn_list), count=count)

plt.clf()
plt.pcolor(count[::-1], cmap=cmap)
plt.yticks(x, phn_list[::-1])
plt.xticks(x, phn_list, rotation=90)
for i, j in product(range(phoneme_N), repeat=2):
    if count[i, j] != 0:
        plt.text(x[j], x[::-1][i], count[i, j], size=pfsize, color=fcolor, verticalalignment="center", horizontalalignment="center")
plt.ylabel("From phoneme")
plt.xlabel("To phoneme")
plt.title("Phoneme bigram")
plt.savefig(output_target_dir / f"Phoneme_bigram.{figure_ext}")
