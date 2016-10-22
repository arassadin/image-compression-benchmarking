from PIL import Image
from glob import glob
import os


DATA_DIR = './examples/'
OUT_DIR = './test_images'
DATA_TMPL = '*'
MIN_BLOCK_SIZE = 5

out_fromats = [
    {'format': 'jpeg', 'params': {'quality': 20}},
    {'format': 'jpeg', 'params': {'quality': 40}},
    {'format': 'jpeg', 'params': {'quality': 60}},
    {'format': 'jpeg', 'params': {'quality': 80}},
    {'format': 'jpeg', 'params': {'optimize': True}},
    {'format':  'png', 'params': {'compress_level': 2}},
    {'format':  'png', 'params': {'compress_level': 4}},
    {'format':  'png', 'params': {'compress_level': 6}},
    {'format':  'png', 'params': {'compress_level': 8}},
    {'format':  'png', 'params': {'optimize': True}},
    {'format': 'webp', 'params': {'quality': 20}},
    {'format': 'webp', 'params': {'quality': 40}},
    {'format': 'webp', 'params': {'quality': 60}},
    {'format': 'webp', 'params': {'quality': 80}},
    {'format': 'webp', 'params': {'lossless': True}}
]

img_files = sorted(glob(os.path.join(DATA_DIR, DATA_TMPL)))

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

for img_file in img_files:
    print '[INFO] Processing \'{}\':'.format(os.path.basename(img_file))
    img = Image.open(img_file)
    print '[INFO]     input image format: {} / {} / {}'.format(img.format, img.mode, img.size)
    height_mp = int(round(img.height / 32.0))
    width_mp = int(round(img.width / 32.0))
    w_add = h_add = 0
    if width_mp > height_mp:
        w_add = width_mp - height_mp
    else:
        h_add = height_mp - width_mp
    for mp in range(MIN_BLOCK_SIZE, min(height_mp, width_mp) + 1):
        img_res = img.resize((32 * (mp + w_add), 32 * (mp + h_add)))
        print '[INFO]     handling size {}x{}:'.format(img_res.width, img_res.height)
        for out_frm in out_fromats:
            out_name = '{}_size={}x{},codec={}'.format(os.path.basename(img_file).rsplit('.')[0],
                                                       img_res.width, img_res.height, out_frm['format'])
            for p, v in out_frm['params'].iteritems():
                out_name += ',{}={}'.format(p, v)
                print '[INFO]         generating {}'.format(out_name)
            img_res.save(os.path.join(OUT_DIR, out_name), format=out_frm['format'], **out_frm['params'])
        out_name = '{}_size={}x{}_orig.ppm'.format(os.path.basename(img_file).rsplit('.')[0], img_res.width,
                                               img_res.height)
        img_res.save(os.path.join(OUT_DIR, out_name), format='ppm')

print '[INFO] Done!'
