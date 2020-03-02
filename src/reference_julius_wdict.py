from pathlib import Path
from argparse import ArgumentParser
import subprocess
# bccwj.60k.htkdic

delimiter = ":="

parser = ArgumentParser()

parser.add_argument("--julius_htkdic", required=True)
parser.add_argument("--target_wdict", type=Path, required=True)

args = parser.parse_args()

wdict_lines = args.target_wdict.read_text().split("\n")
wdict_lines = [l for l in wdict_lines if l]
L = len(wdict_lines)

for i in range(L):
    word = wdict_lines[i].split(delimiter)[0].strip()
    ret_val = subprocess.run(f'cat {str(args.julius_htkdic)} | grep "\[{word}\]"', shell=True, stdout=subprocess.PIPE).stdout

    decoded_ret_val = ret_val.decode("utf-8").split("\n")
    print(len(decoded_ret_val))
    if len(decoded_ret_val) == 1:
        phonemes = input(f"What phonemes of the '{word}'? >> ")
    else:
        phonemes = decoded_ret_val[0].split("\t")[-1]

    wdict_lines[i] = f"{word} {delimiter} {phonemes}"

args.target_wdict.write_text("\n".join(wdict_lines))
