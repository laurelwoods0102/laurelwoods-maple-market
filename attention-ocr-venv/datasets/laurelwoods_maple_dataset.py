import os

from datasets import fsns

DEFAULT_DATASET_DIR = os.path.join(os.path.dirname(__file__), 'laurelwoods-maple-dataset')

DEFAULT_CONFIG = {
    'name':
        'laurelwoods-maple',
    'splits': {
        'train': {
            'size': 29,
            'pattern': 'tfexample_train_resized*'
        },
        'test': {
            'size': 29,
            #'pattern': 'tfexample_test*'
            'pattern': 'tfexample_train_resized*'
        }
    },
    'charset_filename':
        'word_bag_2.txt',
    'image_shape': (300, 200, 3),
    'num_of_views':
        1,
    'max_sequence_length':
        320,
    'null_code':
        0,
    'items_to_descriptions': {
        'image':
            'A [300 x 200 x 3] color image.',
        'label':
            'Characters codes.',
        'text':
            'A unicode string.',
        'length':
            'A length of the encoded text.',
        'num_of_views':
            'A number of different views stored within the image.'
    }
}


def get_split(split_name, dataset_dir=None, config=None):
  if not dataset_dir:
    dataset_dir = DEFAULT_DATASET_DIR
  if not config:
    config = DEFAULT_CONFIG

  return fsns.get_split(split_name, dataset_dir, config)