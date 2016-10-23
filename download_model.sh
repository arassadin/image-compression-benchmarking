#!/bin/bash

echo "[$(date +"%T")] [INFO] Downloading..."
wget -q http://download.tensorflow.org/models/compression_residual_gru-2016-08-23.tar.gz -O /tmp/res_gru.tar.gz 
[[ $? > 0 ]] && { echo "[ERROR] Unable to download model"; exit 1; }
echo "[$(date +"%T")] [INFO] Extracting..."
tar -xzf /tmp/res_gru.tar.gz -C /tmp/
[[ $? > 0 ]] && { echo "[ERROR] Unable to extract model"; exit 1; }
mkdir -p "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/google's-compression-model"
[[ $? > 0 ]] && { echo "[ERROR] Unable to create target folder"; exit 1; }
mv -f /tmp/compression_residual_gru/* "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/google's-compression-model"
[[ $? > 0 ]] && { echo "[ERROR] Unable to store model in target folder"; exit 1; }
rm -rf /tmp/res_gru.tar.gz /tmp/compression_residual_gru/
echo "[$(date +"%T")] [INFO] Done!"
