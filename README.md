# データセット作成支援プログラム群

Author: 尾崎 僚 (Ryo Ozaki)

Required: [Julius](https://github.com/julius-speech/julius) <br>
Required: [Julius Japanese Dictation-kit](https://github.com/julius-speech/dictation-kit)

----
## Julius installation
1. Install julius.
```
git clone https://github.com/julius-speech/julius
cd julius
./configure
make
make install
```
2. Clone Dictation-kit and copy some files
```
git clone https://github.com/julius-speech/dictation-kit
cp -r dictation-kit/model ./
cp dictation-kit/julius.dnnconf ./
```

----
- 書き下し文ファイル
  - 拡張子はtxt
  - 1文1行で記述
  - "[sentence_id]: [word_1] [word_2] ..."と記述
  - 単語間は半角スペースで区切る
- 単語辞書ファイル
  - 拡張子はwdict
  - 1行1単語で記述
  - "単語 := 音素列"と記述

----
## recording.py
書き下し文をもとに音声の録音を行う．

### Usage sample
```
python src/recording.py \
  --chunk <CHUNK> \
  --samplerate <SAMPLERATE> \
  --threshold <THRESHOLD> \
  --sil_margin <SIL_MARGIN> \
  --sentence <SENTENCE> \
  --output_dir <OUTPUT_DIR> \
  --speaker <SPEAKER> \
  --repeat <REPEAT> \
  --randamize
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --sentence | 書き下し文ファイル |
| --output_dir | 出力先ディレクトリ |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --chunk | 1024 | 音声録音時に一度に読み込むチャンク数 |
| --samplerate | 48000 | サンプリングレート |
| --threshold | 0.01 | 無音区間判定に用いる閾値 |
| --sil_margin | 1.0 | 音声ファイルの前後に挿入する無音区間の最小時間 (秒) |
| --speaker | | 指定時は"--output_dir / --speaker"の位置に音声ファイルが保存される |
| --repeat | 1 | 繰り返し回数 |
| --randamize | | 文章をランダムに並び替えて録音を行う |

----
## make_empty_wdict.py
空の単語辞書ファイルを作成する．

### Usage sample
```
python src/make_empty_wdict.py \
  --sentence <SENTENCE> \
  --replace_file
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --sentence | センテンスファイル |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --replace_file | | 既にwdictファイルが存在した時，置き換える |

----
## reference_julius_wdict.py
Juliusの単語辞書を参照し，.wdictファイルを一部埋める．

### Usage sample
```
python src/reference_julius_wdict.py \
  --julius_htkdic <JULIUS_HTKDIC> \
  --target_wdict <TARGET_WDICT>
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --julius_htkdic | .htkdicファイル |
| --target_wdict | .wdict ファイル |

#### Optional arguments
None

----
## make_julius_lang_model.py
書き下し文および単語辞書を参照し，Juliusを用いたラベリングに必要なファイルを作成する．

### Usage sample
```
python src/make_julius_lang_model.py \
  --source <SOURCE> \
  --output_dir <OUTPUT_DIR> \
  --repeat <REPEAT> \
  --BOS <BOS> \
  --EOS <EOS> \
  --AM <ACOUSTIC_MODEL>
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --source | センテンスファイル |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --output_dir | --source | パラメータファイルの出力先ディレクトリ |
| --repeat | 1 | 繰り返し回数 |
| --AM | DNN | 音響モデル (DNN / GMM) |
| --BOS | &lt;s&gt; | 文章開始フラグ単語 |
| --EOS | &lt;/s&gt; | 文章終了フラグ単語 |

----
## make_julius_recognition_script.py
Juliusを用いた音声認識を実行するスクリプトを作成する．

### Usage sample
```
python src/make_julius_recognition_script.py \
  --source_dir <SOURCE_DIR> \
  --lang_model_dir <LANG_MODEL_DIR> \
  --samplerate <SAMPLERATE> \
  --julius_exe <JULIUS_EXE> \
  --output_file <OUTPUT_FILE> \
  --AM <ACOUSTIC_MODEL>
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --source_dir | 認識対象ファイルが配置されているディレクトリ |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --output_file | recognition.sh | Julius 音声認識を実行するスクリプト |
| --lang_model_dir | --source_dir | make_julius_lang_model.py で作成されたパラメータの保存ディレクトリ |
| --samplerate | 48000 | 音声ファイルのサンプリングレート (16000 / 48000) |
| --julius_exe | julius | juliusの実行ファイル (インストール先が通常インストールと異なる場合などで使用) |
| --AM | DNN | 音響モデル (DNN / GMM_mono / GMM_tri) |

----
## convert_julius_label.py
Juliusの認識結果からセグメントファイルを作成する．

### Usage sample
```
python src/convert_julius_label.py \
  --source_dir <SOURCE_DIR> \
  --samplerate <SAMPLERATE> \
  --label_format <LABEL_FORMAT>
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --source_dir | 認識結果ファイルが配置されているディレクトリ |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --samplerate | 48000 | 音声ファイルのサンプリングレート (16000 / 48000) |
| --label_format | time | 出力するラベルのフォーマット (time / wav_frame / mfcc_frame) |

----
## cut_sil_using_label.py
文章前後の無音区間をJuliusを用いた認識ラベルをもとに除去する．

### Usage sample
```
python src/cut_sil_using_label.py \
  --source_dir <SOURCE_DIR> \
  --label_format <LABEL_FORMAT> \
  --output_dir <OUTPUT_DIR>
```
```
python src/cut_sil_using_label.py \
  --source_dir <SOURCE_DIR> \
  --label_format <LABEL_FORMAT> \
  --replace
```

### Arguments
#### Required arguments
| Argument | Help |
|----------|------|
| --source_dir | 認識結果ファイルが配置されているディレクトリ |
| --output_dir <br> --replace | 出力先ディレクトリ <br> 元ファイルを置き換える |

#### Optional arguments
| Argument | Default | Help |
|----------|---------|------|
| --label_format | time | 入力・出力するラベルのフォーマット (time / wav_frame / mfcc_frame) |
