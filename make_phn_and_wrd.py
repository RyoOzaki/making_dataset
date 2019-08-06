from pathlib import Path
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument("source_file", type=Path, help="source file of dataset")

parser.add_argument("-o", "--output_dir", type=Path, default="./source", help="dir of saving summary files and figures")

parser.add_argument("--delimiter", default=":=")
parser.add_argument("--repeat", type=int, default=1)
args = parser.parse_args()

source_file = args.source_file
source_dir = source_file.parent
name = source_file.stem
output_dir = args.output_dir
repeat = args.repeat
delimiter = args.delimiter

output_dir.mkdir(exist_ok=True)

word_dict_file = source_dir / f"{name}.wdict"

sentences = load_sentences(source_file)
word_dict = load_word_dict(word_dict_file, delimiter)

word_list = list(word_dict.keys())
word_list.sort()
phoneme_list = list(set([phoneme for phoneme_seq in word_dict.values() for phoneme in phoneme_seq]))
phoneme_list.sort()

phn_sentences = []
wrd_sentences = []

for i in range(repeat):
    for sentence in sentences:
        phn_sentence = []
        wrd_sentence = []
        for word in sentence:
            phn_sentence.extend([phoneme_list.index(p) for p in word_dict[word]])
            wrd_sentence.extend([word_list.index(word)] * len(word_dict[word]))
        phn_sentences.append(phn_sentence)
        wrd_sentences.append(wrd_sentence)

chr_out_file = output_dir / f"{name}.chr"
wrd_out_file = output_dir / f"{name}.wrd"

print(f"Phoneme N: {len(phoneme_list)}")
print(f"Word N: {len(word_list)}")

chr_out_file.write_text("\n".join([" ".join([str(e) for e in sentence]) for sentence in phn_sentences]))
wrd_out_file.write_text("\n".join([" ".join([str(e) for e in sentence]) for sentence in wrd_sentences]))
