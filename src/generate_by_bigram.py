import numpy as np
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("source_file", type=Path, help="source file of bigram (npz)")

parser.add_argument("-n", "--num_of_gen", type=int, default=1, help="number of generate samples")

parser.add_argument("--delimiter", type=str, default=" ", help="delimiter of words")
parser.add_argument("--write_flags", action="store_true", help="write BOS (begin of sentence, <s>) and EOS (end of sentence, </s>)")

args = parser.parse_args()

source_file = args.source_file
num = args.num_of_gen
delimiter = args.delimiter
write_flags = args.write_flags

npz_obj = np.load(source_file)
list_key = [key for key in npz_obj.keys() if key.endswith("_list")][0]

item_list = list(npz_obj[list_key])
counts = npz_obj["count"].astype(float)

sum_v = counts.sum(axis=1)
row_flags = (sum_v != 0)

counts[row_flags] /= sum_v[row_flags].reshape((-1, 1))

for n in range(num):
    item = "<s>"
    sentence = []
    while True:
        sentence.append(item)
        if item == "</s>":
            break
        prob = counts[item_list.index(item)]
        item = np.random.choice(item_list, p=prob)
    if not write_flags:
        sentence = sentence[1:-1]
    print(delimiter.join(sentence))
