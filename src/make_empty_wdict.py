from pathlib import Path
import argparse
from utility.loads import load_sentences

separator = " "
delimiter = ":="
wdict_ext = "wdict"

parser = argparse.ArgumentParser()
parser.add_argument("--source_file", required=True, type=Path, help="source file of dataset")

parser.add_argument("--replace_file", action="store_true", help="replace wdict file if already exists")

args = parser.parse_args()

source_file = args.source_file
source_dir = source_file.parent
replace_file = args.replace_file

print(f"Processing {source_file}")

words = set()
for snt in load_sentences(args.source_file):
    words |= set(snt)
words = list(words)
words.sort()

body = [
    f"{word} {delimiter} "
    for word in words
]
print(f"Word N: {len(words)}")

out_file = source_file.with_name(f"{source_file.stem}.{wdict_ext}")
if replace_file is False:
    idx = 0
    while out_file.exists():
        out_file = source_file.with_name(f"{source_file.stem}_{idx}.{wdict_ext}")
        idx += 1
out_file.write_text("\n".join(body))
print(f"{out_file}に空の単語辞書ファイルを作成しました．")
