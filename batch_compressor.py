from os import *
from multiprocessing import Pool
from subprocess import call

def compress(filename):
	call(['python', 'nn_compression_example.py', '--image=test_images/' + filename, '--quality=15', '--model=residual_gru.pb'])
#python nn_compression_example.py --image=cat_size\=160x416\,codec\=webp\,lossless\=True --quality=15 --model=residual_gru.pb

if __name__ == '__main__':
	originals = [f for f in listdir('test_images') if f.endswith('lossless=True')]
	for imagename in originals:
		compress(imagename)		

# if you have a lot of resources
#	pool = Pool(processes = 4)              # process per core
#	pool.map(compress, originals)
	