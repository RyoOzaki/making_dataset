from pathlib import Path
import argparse

separator = " "
delimiter = ":="
wdict_ext = "wdict"
source_ext = "txt"

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source_dir", type=Path, default="./source", help="root dir of source data, i.e., '*.wdict' and '*.txt'")
parser.add_argument("-n", "--name", type=str, required=True, help="target datasets name")
args = parser.parse_args()

source_dir = args.source_dir
name = args.name

source_dir = args.source_dir
name = args.name

target_file = source_dir / f"{name}.{source_ext}"

print(f"Processing {target_file}")

tmp = target_file.read_text().replace("\n", separator).split(separator)
words = list(set([w for w in tmp if w]))
words.sort()

body = [
    f"{word} {delimiter} "
    for word in words
]
print(f"Word N: {len(words)}")

out_file = source_dir / f"{name}.{wdict_ext}"
idx = 0
while out_file.exists():
    out_file = source_dir / f"{name}_{idx}.{wdict}"
    idx += 1
out_file.write_text("\n".join(body))
print(f"{out_file}に空の単語辞書ファイルを作成しました．")
