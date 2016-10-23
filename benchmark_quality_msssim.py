import os
import sys
sys.path.append('google')
from msssim import MultiScaleSSIM
from PIL import Image
import numpy as np
from glob import glob
import cv2
import time


ORIGINAL_TMPL = '*_orig.ppm'
SAMPLES_DIR = 'test_images'
RESULTS_DIR = '_benchmarks_'

def compare(img1, img2):
    img1 = np.expand_dims(img1, 0)
    img2 = np.expand_dims(img2, 0)
    return MultiScaleSSIM(img1, img2)

def generate_header():
    return 'source;size;params;metric\n'

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

results_file = open(os.path.join(RESULTS_DIR, 'quality_msssim.csv'), 'w')
results_file.write(generate_header())
results_file.flush()

def main():
    files_original = sorted(glob(os.path.join(SAMPLES_DIR, ORIGINAL_TMPL)))
    imgs_names = {}
    for i_f, img_f in enumerate(files_original):
        name = os.path.basename(img_f).split('_')[0]
        if imgs_names.get(name, None) is None:
            imgs_names[name] = [i_f]
        else:
            imgs_names[name].append(i_f)

    for name, inds in sorted(imgs_names.iteritems()):
        print '[{}] [INFO] Processing \'{}\' derivatives:'.format(time.strftime("%H:%M:%S"),
                                                                 name)
        files_samesource_orig = [f for i, f in enumerate(files_original) if i in inds]

        imgs_sizes = {}
        for i_f, img_f in enumerate(files_samesource_orig):
            img_f = os.path.basename(img_f)
            start = img_f.find('{}='.format('size'))
            size = img_f[start:].split('_')[0][5:]
            if imgs_sizes.get(size, None) is None:
                imgs_sizes[size] = i_f
            else:
                print '[{}] [WARNING] '.format(time.strftime("%H:%M:%S")) + \
                      'Multiple uncompressed images with equal sizes. Only first one will be used.'
        sizes = imgs_sizes.keys()

        def size_ordering(size):
            s1 = int(size.split('x')[0])
            s2 = int(size.split('x')[1])
            return s1 * s2
        sizes = sorted(sizes, key=size_ordering)

        for size in sizes:
            print '[{}] [INFO]     handling resolution \'{}\''.format(time.strftime("%H:%M:%S"),
                                                                       size)
            file_orig = files_samesource_orig[imgs_sizes[size]]
            img_orig = cv2.cvtColor(cv2.imread(file_orig), cv2.COLOR_BGR2RGB)

            files_samesize = glob(os.path.join(SAMPLES_DIR, '{}_*{}*'.format(name, size)))
            files_samesize = [f for f in files_samesize if f not in files_samesource_orig]
            for f in files_samesize:
                print '[{}] [INFO]         found \'{}\''.format(time.strftime("%H:%M:%S"),
                                                                os.path.basename(f))
                img_cmp = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2RGB)
                diff = compare(img_orig, img_cmp)
                cmp_params = ''.join(os.path.basename(f).split('_')[1:])
                start = cmp_params.find('size=')
                cmp_params = cmp_params[:start] + cmp_params[start + 5 + len(size) + 1 : ]
                results_file.write('{};{};{};{}\n'.format(name, size, cmp_params, diff))
                results_file.flush()
    print '[{}] [INFO] Done!'.format(time.strftime("%H:%M:%S"))

if __name__ == '__main__':
    main()