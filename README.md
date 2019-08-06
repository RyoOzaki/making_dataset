# データセット作成支援プログラム群

Author: 尾崎 僚 (Ryo Ozaki)

---
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

---

## make_empty_wdict.py
単語辞書ファイルを空で作成

### 引数一覧
|引数                |デフォルト値         |備考|
|-------------------|-------------------|---|
| -s (--source_dir) | ./source          | 書き下し文のあるディレクトリ |
| -n (--name)       | なし（必須）        | 書き下し文のファイル名 (拡張子除く) |

### 実行方法サンプル
```
python make_empty_wdict.py -n sample
python make_empty_wdict.py -s source -n sample
```

---

## analyze.py
書き下し文・単語辞書から単語のバイクラムや単語頻度・音素頻度等を図・ファイルに保存

### 引数一覧
|引数                |デフォルト値         |備考|
|-------------------|-------------------|---|
| -s (--source_dir) | ./source          | 書き下し文のあるディレクトリ |
| -n (--name)       | なし（必須）        | 書き下し文のファイル名 (拡張子除く) |
| -o (--output)     | ./analyze_summary | 出力先ディレクトリ|
|--figure_ext       | png               | 出力する図の拡張子 |
|--delimiter        | :=                | 単語の定義演算子 |
|--repeat           | 1                 | 書き下し文の繰り返し回数 |
|--pfsize           | 10                | 音素バイグラム・単語辞書のフォントサイズ |
|--wfsize           | 10                | 単語バイグラムのフォントサイズ |
|--fcolor           | black             | バイグラム・単語辞書のフォントカラー |
|--cmap             | rainbow           | バイグラム・単語辞書のカラーマップ |

### 実行方法サンプル
```
python analyze -n sample
python analyze -s source -o analyze_summary -n sample
python analyze -n sample --delimiter := --repeat 1
```

---

## make_synthetic_data.py
書き下し文・単語辞書から2次元ガウス分布のデータセットを作成

### 引数一覧
|引数                |デフォルト値         |備考|
|-------------------|-------------------|---|
| -s (--source_dir) | ./source          | 書き下し文のあるディレクトリ |
| -n (--name)       | なし（必須）        | 書き下し文のファイル名 (拡張子除く) |
| -o (--output)     | ./synthetic_data  | 出力先ディレクトリ|
|--delimiter        | :=                | 単語の定義演算子 |
|--repeat           | 1                 | 書き下し文の繰り返し回数 |

### 実行方法サンプル
```
python make_synthetic_data.py -n sample
python make_synthetic_data.py -s source -o synthetic_data -n sample
python make_synthetic_data.py -n sample --delimiter := --repeat 1
```
