import os
import numpy as np
import tensorflow as tf
from PIL import Image
import time

tf.flags.DEFINE_string('image', None, 'Location of image to compress.')
tf.flags.DEFINE_integer('quality', 8, 'Compression level.'
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
    if FLAGS.image is None:
        print ('\nUsage: python nn_compression_example.py '
               '--image=/path/to/image '
               '--quality=0|...|15 '
               '--model=residual_gru.pb\n')
        return

    if FLAGS.quality < 0 or FLAGS.quality > 15:
        print '[{}] [ERROR] Quality must be between 0 and 15 inclusive.'.format(time.strftime('%H:%M:%S'))
        return

    with tf.Graph().as_default() as graph:
        print '[{}] [INFO] Loading model'.format(time.strftime('%H:%M:%S'))
        with open(FLAGS.model, 'rb') as model:
          graph_def = tf.GraphDef()
          graph_def.ParseFromString(model.read())
        _ = tf.import_graph_def(graph_def, name='')

        input_tensor = graph.get_tensor_by_name('Placeholder:0')
        outputs_enc = [graph.get_tensor_by_name(name) for name in
                       get_output_tensor_names_enc()]

        input_tensors = outputs_enc[0 : FLAGS.quality + 1]
        outputs_dec = [graph.get_tensor_by_name(name) for name in
                       get_output_tensor_names_dec()][0 : FLAGS.quality + 1]

        img = np.array(Image.open(FLAGS.image))
        print '[{}] [INFO] Processing \'{}\' for quality {}'.format(time.strftime('%H:%M:%S'),
                                                                    os.path.basename(FLAGS.image),
                                                                    FLAGS.quality)

        print '[{}] [INFO]     Performing compression'.format(time.strftime('%H:%M:%S'))
        with tf.Session(graph=graph) as sess:
########### encoding
            img_array = sess.run(tf.convert_to_tensor(np.expand_dims(img, axis=0)))
            results_enc = sess.run(outputs_enc, feed_dict={input_tensor: img_array})
            results_enc = results_enc[0 : FLAGS.quality + 1]
            int_codes = [x.astype(np.int8) for x in results_enc]
            print '[{}] [INFO]         encoding done'.format(time.strftime("%H:%M:%S"))

########### decoding
            feed_dict = dict(zip(input_tensors, int_codes))
            results_dec = sess.run(outputs_dec, feed_dict=feed_dict)
            print '[{}] [INFO]         decoding done'.format(time.strftime("%H:%M:%S"))

        img_compressed = np.uint8(np.clip(results_dec[-1] + 0.5, 0, 255))
        img_compressed = img_compressed.squeeze()
        out_name = os.path.basename(FLAGS.image).rsplit('.')
        out_path = os.path.join(os.path.dirname(FLAGS.image),
                                '{}_compressed_quality={}.{}'.format(''.join(out_name[:-1]),
                                                                 FLAGS.quality,
                                                                 out_name[-1]
                                                                 )
                                )
        print '[{}] [INFO]         saving \'{}\''.format(time.strftime('%H:%M:%S'),
                                                         os.path.basename(out_path))
        Image.fromarray(img_compressed).save(out_path, format='ppm')
    print '[{}] [INFO] Done!'.format(time.strftime('%H:%M:%S'))

if __name__ == '__main__':
    tf.app.run()
