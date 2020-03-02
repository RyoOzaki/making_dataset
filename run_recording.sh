#!/bin/bash

TARGET="sentences/murakami_data.txt"
SPEAKER="speaker_1"

python src/recording.py \
  --sentence ${TARGET} \
  --output_dir raw_source \
  --speaker ${SPEAKER} \
  --randamize
