#!/bin/bash

TARGET="sentences/murakami_data.txt"
LABEL_FORMAT="time"

SOURCE_DIR="./raw_source"
OUTPUT_DIR="./source"

# DNN
# AM_BASE="DNN"
# AM_SUB="DNN"

# GMM-triphone
AM_BASE="GMM"
AM_SUB="GMM_tri"

# GMM-monophone
# AM_SUB="GMM"
# AM_SUB="GMM_mono"

python src/make_julius_lang_model.py \
  --source ${TARGET} \
  --output_dir julius_lang_model \
  --AM ${AM_BASE}

python src/make_julius_recognition_script.py \
  --source_dir ${SOURCE_DIR} \
  --lang_model_dir julius_lang_model \
  --output_file recognition.sh \
  --AM ${AM_SUB}

bash recognition.sh

python src/convert_julius_label.py \
  --label_format ${LABEL_FORMAT}

python src/cut_sil_using_label.py \
  --source_dir ${SOURCE_DIR} \
  --label_format ${LABEL_FORMAT} \
  --output_dir ${OUTPUT_DIR}
