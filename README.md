# データセット作成支援プログラム群

Author: 尾崎 僚 (Ryo Ozaki)

## 前提
- 書き下し文ファイル
  - 拡張子はtxt
  - 1文1行で記述
  - 単語間は半角スペースで区切る
- 単語辞書ファイル
  - 拡張子はwdict
  - 1行1単語で記述
  - "単語 := 音素列"のフォーマットに従って記述
    - (ただし定義記号":="は引数--delimiterにより変更可)

## make_empty_wdict.py
単語辞書ファイルを空で作成

### 位置引数一覧
|位置                |備考|
|-------------------|---|
| 1                 | 書き下し文のファイル |

### オプション引数一覧
|オプション           |デフォルト値         |備考|
|-------------------|-------------------|---|
| --replace_file    | False             | オプション指定でファイルを上書き |
### 実行方法サンプル
```
python make_empty_wdict.py source/sample.txt
python make_empty_wdict.py source/sample.txt --replace_file
```

## analyze.py
書き下し文・単語辞書から単語のバイクラムや単語頻度・音素頻度等を図・ファイルに保存

### 位置引数一覧
|位置                |備考|
|-------------------|---|
| 1                 | 書き下し文のファイル |


### オプション引数一覧
|オプション           |デフォルト値         |備考|
|-------------------|-------------------|---|
| -o (--output)     | ./analyze_summary | 出力先ディレクトリ |
| --figure_ext      | png               | 出力する図の拡張子 |
| --delimiter       | :=                | 単語の定義演算子 |
| --repeat          | 1                 | 書き下し文の繰り返し回数 |
| --pfsize          | 10                | 音素バイグラム・単語辞書のフォントサイズ |
| --wfsize          | 10                | 単語バイグラムのフォントサイズ |
| --fcolor          | black             | バイグラム・単語辞書のフォントカラー |
| --cmap            | rainbow           | バイグラム・単語辞書のカラーマップ |

### 実行方法サンプル
```
python analyze.py source/sample.txt
python analyze.py source/sample.txt -o analyze_summary
python analyze.py source/sample.txt --delimiter := --repeat 1
```

## make_synthetic_data.py
書き下し文・単語辞書から2次元ガウス分布のデータセットを作成

### 位置引数一覧
|位置                |備考|
|-------------------|---|
| 1                 | 書き下し文のファイル |

### オプション引数一覧
|オプション           |デフォルト値         |備考|
|-------------------|-------------------|---|
| -o (--output)     | ./synthetic_data  | 出力先ディレクトリ|
| --delimiter       | :=                | 単語の定義演算子 |
| --repeat          | 1                 | 書き下し文の繰り返し回数 |

### 実行方法サンプル
```
python make_synthetic_data.py source/sample.txt
python make_synthetic_data.py source/sample.txt -o synthetic_data
python make_synthetic_data.py source/sample.txt --delimiter := --repeat 1
```

## make_phn_and_wrd.py
latticelm用に書き下し文・単語辞書からphnファイルとwrdファイルを作成

### 位置引数一覧
|位置                |備考|
|-------------------|---|
| 1                 | 書き下し文のファイル |

### オプション引数一覧
|オプション           |デフォルト値         |備考|
|-------------------|-------------------|---|
| -o (--output)     | ./source          | 出力先ディレクトリ|
| --delimiter       | :=                | 単語の定義演算子 |
| --repeat          | 1                 | 書き下し文の繰り返し回数 |

### 実行方法サンプル
```
python make_phn_and_wrd.py source/sample.txt
python make_phn_and_wrd.py source/sample.txt -o synthetic_data
python make_phn_and_wrd.py source/sample.txt --delimiter := --repeat 1
```
