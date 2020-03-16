# ライブラリの読込
import pyaudio
import wave
import array
import numpy as np
import random
from pathlib import Path
import time
from argparse import ArgumentParser
from utility.loads import load_sentences, load_stems

# 音データフォーマット
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
threshold = 0.01
sil_margin_sec = 1.0 # sec

parser = ArgumentParser()
parser.add_argument("--chunk", type=int, default=chunk)
parser.add_argument("--samplerate", type=int, help="Sampling rate", default=RATE)
parser.add_argument("--threshold", type=float, help="Threshold of recording", default=threshold)
parser.add_argument("--sil_margin", type=float, help="margin of silent time [sec]", default=sil_margin_sec)

parser.add_argument("--sentence", type=Path, required=True)
parser.add_argument("--output_dir", type=Path, required=True)
parser.add_argument("--speaker")
parser.add_argument("--randamize", action="store_true")
parser.add_argument("--repeat", type=int, default=1)
parser.add_argument("--without_check", action="store_true")

args = parser.parse_args()

if args.speaker is None:
    output_dir = args.output_dir
else:
    output_dir = args.output_dir / args.speaker
output_dir.mkdir(exist_ok=True, parents=True)

sentences = load_sentences(args.sentence, repeat=args.repeat)
stems = load_stems(args.sentence, repeat=args.repeat)
stems_sentences = list(zip(stems, sentences))
if args.randamize:
    random.shuffle(stems_sentences)

chunk = args.chunk
RATE = args.samplerate
threshold = args.threshold
sil_margin_sec = args.sil_margin

sil_margin_cnt = int(RATE / chunk * int(sil_margin_sec))

# 音の取込開始
p = pyaudio.PyAudio()
in_stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)
in_stream.stop_stream()

out_stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    output = True,
    frames_per_buffer = chunk
)
out_stream.stop_stream()

S = len(stems_sentences)
s = 0
while s < S:
    stm, snt = stems_sentences[s]
    in_stream.start_stream()
    heads = []
    for _ in range(sil_margin_cnt):
        heads.append(in_stream.read(chunk))
    print(f"Please speech <<< {snt} >>>")
    while True:
        # 音データの取得
        data = in_stream.read(chunk)
        heads.append(data)
        # ndarrayに変換
        x = np.frombuffer(data, dtype="int16") / 32768.0

        # 閾値以上の場合はファイルに保存
        if x.max() > threshold:
            break

    sil_cnt = 0
    body = []
    print("Recording start!")
    while sil_cnt < sil_margin_cnt:
        # 音データの取得
        data = in_stream.read(chunk)
        body.append(data)
        # ndarrayに変換
        x = np.frombuffer(data, dtype="int16") / 32768.0
        if x.max() <= threshold:
            sil_cnt += 1
        else:
            sil_cnt = 0
    tail = in_stream.read(chunk)
    in_stream.stop_stream()
    all = [*heads[-sil_margin_cnt:], *body, tail]
    print("Preprocessing...")
    all_data = b''.join(all)

    xall = np.frombuffer(all_data, dtype="int16")

    # xall = np.concatenate((np.zeros((sil_margin_cnt*chunk, ), dtype="int16"), xall), axis=0)

    if args.without_check:
        flag = "y"
    else:
        flag = "p"
        while flag not in ["y", "n"]:
            if flag == "p":
                print(f"Playing <<< {snt} >>>")
                out_stream.start_stream()
                out_stream.write(all_data)
                out_stream.stop_stream()
            flag = input("save? (y/n/p) >> ")
    if flag == "y":
        # 音声ファイルとして出力
        filename = str(output_dir / f"{stm}.wav")
        out = wave.open(filename, 'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2) # 16 bits = 2 bytes
        out.setframerate(RATE)
        out.writeframes(array.array("h", xall).tostring())
        out.close()
        s += 1

in_stream.close()
out_stream.close()
p.terminate()
