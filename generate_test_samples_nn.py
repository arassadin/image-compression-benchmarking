import os
import numpy as np
import tensorflow as tf
from glob import glob
from PIL import Image
import cv2
import time


tf.flags.DEFINE_string('image_tmpl', 'test_images/*_orig.ppm', 'Images to compress.')
tf.flags.DEFINE_string('quality', '3,6,9,12', 'List of comression levels, separeted by comma'
                       'Must be between 0 and 15 inclusive.')
tf.flags.DEFINE_string('model', 'google\'s-compression-model/residual_gru.pb',
                       'Location of compression model.')
FLAGS = tf.flags.FLAGS


def get_output_tensor_names_enc():
    name_list = ['GruBinarizer/SignBinarizer/Sign:0']
    for i in xrange(1, 16):
        name_list.append('GruBinarizer/SignBinarizer/Sign_{}:0'.format(i))
    return name_list

def get_output_tensor_names_dec():
    return ['loop_{0:02d}/add:0'.format(i) for i in xrange(0, 16)]

def main(_):

    qualities = [int(q) for q in FLAGS.quality.strip().replace(' ', '').split(',')]

    for q in qualities:
        if q < 0 or q > 15:
            print '[{}] [ERROR] Quality must be between 0 and 15 inclusive.'.format(time.strftime("%H:%M:%S"))
            return

    with tf.Graph().as_default() as graph:
        print '[{}] [INFO] Loading model'.format(time.strftime("%H:%M:%S"))
        with open(FLAGS.model, 'rb') as model:
          graph_def = tf.GraphDef()
          graph_def.ParseFromString(model.read())
        _ = tf.import_graph_def(graph_def, name='')

        input_tensor = graph.get_tensor_by_name('Placeholder:0')
        outputs_enc = [graph.get_tensor_by_name(name) for name in
                       get_output_tensor_names_enc()]

        input_tensors = outputs_enc[0 : max(qualities) + 1]
        outputs_dec = [graph.get_tensor_by_name(name) for name in
                       get_output_tensor_names_dec()][0 : max(qualities) + 1]

        img_files = sorted(glob(FLAGS.image_tmpl))
        imgs_sizes = {}
        for i_f, img_f in enumerate(img_files):
            start = img_f.find('size=')
            size = img_f[start:].split('_')[0][5:]
            if imgs_sizes.get(size, None) is None:
                imgs_sizes[size] = [i_f]
            else:
                imgs_sizes[size].append(i_f)

        for size_ind in imgs_sizes.itervalues():
            images = []
            tmp_fnames = []
            for ind in size_ind:
                img = cv2.cvtColor(cv2.imread(img_files[ind]), cv2.COLOR_BGR2RGB)
                images.append(img)
                tmp_fnames.append(os.path.basename(img_files[ind]))
            images = np.asarray(images, dtype=np.uint8)
            print '[{}] [INFO] Processing {} images: \'{}\' for qualities {}'.format(time.strftime('%H:%M:%S'), 
                                                                                     len(size_ind),
                                                                                     '\', \''.join(tmp_fnames),
                                                                                     # ', '.join([str(q) for q in qualities]))
                                                                                     sorted(qualities))

            print '[{}] [INFO]     Performing compression'.format(time.strftime("%H:%M:%S"))
            with tf.Session(graph=graph) as sess:
############### encoding
                img_array = sess.run(tf.convert_to_tensor(images))
                results_enc = sess.run(outputs_enc, feed_dict={input_tensor: img_array})
                results_enc = results_enc[0 : max(qualities) + 1]
                int_codes = [x.astype(np.int8) for x in results_enc]
                print '[{}] [INFO]         encoding done'.format(time.strftime("%H:%M:%S"))

############### decoding
                feed_dict = dict(zip(input_tensors, int_codes))
                results_dec = sess.run(outputs_dec, feed_dict=feed_dict)
                print '[{}] [INFO]         decoding done'.format(time.strftime("%H:%M:%S"))

            for q in qualities:
                img_compressed = np.clip(results_dec[q] + 0.5, 0, 255).astype(np.uint8)
                for i in xrange(img_compressed.shape[0]):
                    out_name = os.path.basename(img_files[size_ind[i]]).rsplit('.')
                    out_path = os.path.join(
                                            os.path.dirname(img_files[size_ind[i]]),
                                            '{},codec=nn,quality={}.ppm'.format(
                                                                                ''.join(out_name[:-1])[:-5],
                                                                                q
                                                                                )
                                            )
                    print '[{}] [INFO]         saving \'{}\''.format(time.strftime("%H:%M:%S"),
                                                                    os.path.basename(out_path))
                    cv2.imwrite(out_path,
                                cv2.cvtColor(img_compressed[i], cv2.COLOR_RGB2BGR))
    print '[{}] [INFO] Done!'.format(time.strftime('%H:%M:%S'))

if __name__ == '__main__':
    tf.app.run()
