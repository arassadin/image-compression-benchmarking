from os import listdir, path
import tensorflow as tf
import sys
sys.path.append('google')
from msssim import MultiScaleSSIM
import cv2
from PIL import Image
from numpy import expand_dims, asarray

def compare(img1_name, img2_name):
	img1 = expand_dims(asarray(Image.open(img1_name)), 0)
	img2 = expand_dims(asarray(Image.open(img2_name)), 0)
	return MultiScaleSSIM(img1, img2, max_val=255)
	#python nn_compression_example.py --image=cat_size\=160x416\,codec\=webp\,lossless\=True --quality=15 --model=residual_gru.pb
	
def extract_params_from_name(filename):
	parts = filename.split(',')
	codec = parts[1].split('=')[1]
	quality = parts[2].split('=')[1]
	return codec, quality

if __name__ == '__main__':
	for folder in listdir('compressed')[0:1]:
		results = []
		original_path = path.join('test_images', folder + ',codec=webp,lossless=True')
		for image in listdir(path.join('compressed', folder)):
			results.append(';'.join( [image, 'res_gru' , image.split('_')[0], str(compare(path.join('compressed', folder, image), original_path)) ] ))
			#print image, compare(path.join('compressed', folder, image), original_path)
		for image in listdir('test_images'):
			if image.startswith(folder) and not image.endswith('lossless=True'):
				compressed_image = path.join('test_images', image)
				codec, quality = extract_params_from_name(image)
				results.append(';'.join( [image, codec , quality, str(compare(compressed_image, original_path)) ] ))
# 				print image, compare(compressed_image, original_path)
		with open('results.csv', 'a') as result_csv:
			for s in results:
				result_csv.write(s + '\n')
# 	
