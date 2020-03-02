import numpy as np
from pathlib import Path
from argparse import ArgumentParser
from utility.loads import load_word_dict, load_sentences, load_stems

def convert_word_dict_module(phonemes):
    if len(phonemes) == 1:
        return [f"{phonemes[0]}_S", ]
    else:
        first_phn = f"{phonemes[0]}_B"
        middle_phns = [f"{phn}_I" for phn in phonemes[1:-1]]
        final_phn = f"{phonemes[-1]}_E"
        return [first_phn, *middle_phns, final_phn]

def convert_word_dict(word_dict):
    return {wrd: convert_word_dict_module(phns) for wrd, phns in word_dict.items()}

wdict_ext = "wdict"
delimiter = ":="

parser = ArgumentParser()
parser.add_argument("--source", type=Path, required=True, help="source file of dataset")

parser.add_argument("--output_dir", type=Path)

parser.add_argument("--repeat", type=int, default=1, help="repeat count of sentence in source file")

parser.add_argument("--BOS", default="<s>")
parser.add_argument("--EOS", default="</s>")

parser.add_argument("--AM", choices=["GMM", "DNN"], default="DNN")

args = parser.parse_args()

source_file = args.source
source_dir = source_file.parent
output_dir = source_dir if args.output_dir is None else args.output_dir
target_name = source_file.stem

repeat = args.repeat

output_dir.mkdir(exist_ok=True)

wdict_file = source_dir / f"{target_name}.{wdict_ext}"

word_dict = load_word_dict(wdict_file, delimiter)

if args.AM == "DNN":
    word_dict[args.BOS] = ["sp", ]
    word_dict[args.EOS] = ["sp", ]
    word_dict = convert_word_dict(word_dict)
else:
    word_dict[args.BOS] = ["silB", ]
    word_dict[args.EOS] = ["silE", ]

if repeat == 1:
    sentences = load_sentences(source_file)
    stems = load_stems(source_file)
else:
    sentences_tmp = load_sentences(source_file)
    stems_tmp = load_stems(source_file)
    sentences = [snt for snt in sentences_tmp for r in range(repeat)]
    stems = [f"{stem}_{r+1}" for stem in stems_tmp for r in range(repeat)]

sentences = [[args.BOS, *snt, args.EOS] for snt in sentences]

for snt, stm in zip(sentences, stems):

    snt_file = output_dir / f"{stm}.snt"
    dfa_file = output_dir / f"{stm}.dfa"
    dict_file = output_dir / f"{stm}.dict"

    N = len(snt)

    snt_file.write_text(" ".join(snt))

    dict_lines = [
        f"{n} [{wrd}] {' '.join(word_dict[wrd])}"
        for n, wrd in enumerate(snt)
    ]
    dict_file.write_text("\n".join(dict_lines))

    dfa_lines = [
        f"{n} {N-n-1} {n+1} 0 0"
        for n in range(N)
    ]
    dfa_lines.append(
        f"{N} -1 -1 1 0"
    )
    dfa_file.write_text("\n".join(dfa_lines))
