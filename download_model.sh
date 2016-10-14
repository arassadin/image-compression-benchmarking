echo "Downloading..."
wget -q http://download.tensorflow.org/models/compression_residual_gru-2016-08-23.tar.gz -O /tmp/res_gru.tar.gz 
echo "Extracting..."
tar -xzf /tmp/res_gru.tar.gz -C /tmp/
mkdir -p "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/google's-compression-model"
mv -f /tmp/compression_residual_gru/* "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/google's-compression-model"
rm -rf /tmp/res_gru.tar.gz /tmp/compression_residual_gru/
echo "Done!"
