#!/bin/bash

echo "[$(date +"%T")] Generating test images using regular codecs"
python generate_test_samples_regular.py
[[ $? > 0 ]] && { echo "[$(date +"%T")] [ERROR] Unable to generate test samples with regular encoders"; exit 1; }
echo "[$(date +"%T")] Generating test images using nn compression"
python generate_test_samples_nn.py
[[ $? > 0 ]] && { echo "[$(date +"%T")] [ERROR] Unable to generate samples with nn encoding"; exit 1; }
