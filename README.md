# Image Compression Benchmarking

This project inspired by Google's paper ***Full Resolution Image Compression with Recurrent Neural Networks*** ([arxiv](https://arxiv.org/abs/1608.05148)) and its TensorFlow [implementation](https://github.com/tensorflow/models/tree/master/compression).

The code inside aims to compare (quantitatively and qualitatively) different aspects compression done by this *Method* and codecs popular today, in different compression levels, for different image sizes.

# Requirements

Hardware:

* **GPU is not necessary** but preferable
* At least 3Gb of RAM

Software:

* [Ubuntu](https://www.ubuntu.com/) 14.04+ (tested)
* [TensorFlow](https://www.tensorflow.org/)
* [Pillow](https://python-pillow.org/) 3.4+
* [NumPy](http://www.numpy.org/) 1.11+

# Installation

1. First, install suitable TensorFlow version. See instruction [here](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/g3doc/get_started/os_setup.md).

2. Install other project dependencies:

    `./install_deps.sh`

# HowTo

* First, download Google's pre-trained model via `download_model.sh`

* Run `generate_test_samples.sh` **or** `python generate_test_samples_regular.py`, `generate_test_samples_nn.py` **successively**. It will generate a bunch of samples compressed using regular codecs (like *jpeg*, *png* etc.) and also *NN*-based method.

# Results

# License
All files in *google* subfolder have a license from the original project and was taken from tensorflow/models@76739168f61dd9bb849e500bbd235fa9e4b7612f .

License for the google's compression model (*google's-compression-model*) described in its **LICENSE** file.

Images for this project taken from the publicly available datasets, precisely

* [Public-Domain Test Images for Homeworks and Projects](http://homepages.cae.wisc.edu/~ece533/images/)
* [Kodak Lossless True Color Image Suite](http://r0k.us/graphics/kodak/)

All files, that are the heritage of the project, subjects to WTFPL (see **LICENSE** file in the root).