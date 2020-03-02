import numpy as np
from argparse import ArgumentParser
from pathlib import Path
import subprocess

parser = ArgumentParser()

parser.add_argument("--source_dir", type=Path, required=True)
parser.add_argument("--lang_model_dir", type=Path)
parser.add_argument("--samplerate", type=int, default=48000, choices=[16000, 48000])
parser.add_argument("--julius_exe", default="julius")

parser.add_argument("--output_file", type=Path, default="recognition.sh")
parser.add_argument("--AM", choices=["GMM_mono", "GMM_tri", "DNN"], default="DNN")

args = parser.parse_args()

if args.AM == "DNN":
    julius_param_conf = "julius.dnnconf"
    julius_param_h = "model/dnn/binhmm.SID"
    julius_param_hlist = "model/dnn/logicalTri.bin"
elif args.AM == "GMM_tri":
    julius_param_h = "model/phone_m/jnas-tri-3k16-gid.hmmdefs"
    julius_param_hlist = "model/phone_m/logicalTri-3k16-gid.bin"
else:
    julius_param_h = "model/phone_m/jnas-mono-16mix-gid.hmmdefs"
    # julius_param_hlist = "model/phone_m/logicalTri-3k16-gid.bin"

lang_model_dir = args.source_dir if args.lang_model_dir is None else args.lang_model_dir

files = args.source_dir.glob(f"**/*.wav")
files = sorted(files, key=str)

commands = []
commands.append("#!/bin/bash")
for file in files:
    command = []
    command.append(f"echo '{str(file)}'")
    command.append(f"|")
    command.append(f"{args.julius_exe}")
    command.append(f"-h {julius_param_h}")
    if args.AM != "GMM_mono":
        command.append(f"-hlist {julius_param_hlist}")
    if args.AM =="DNN":
        command.append(f"-dnnconf {julius_param_conf}")
    if args.samplerate == 48000:
        command.append(f"-48")
    command.append(f"-dfa {lang_model_dir / file.stem}.dfa")
    command.append(f"-v {lang_model_dir / file.stem}.dict")
    command.append(f"-walign")
    command.append(f"-palign")
    command.append(f"-nostrip")
    command.append(f"-input file")
    command.append(f"-outfile")

    commands.append(" ".join(command))

args.output_file.parent.mkdir(exist_ok=True, parents=True)
args.output_file.write_text("\n".join(commands))
