import argparse
from mmseg.apis import inference_segmentor, init_segmentor
import cv2
import numpy as np

CLASSES = ('background', 'aeroplane', 'bag', 'bed', 'bedclothes', 'bench',
               'bicycle', 'bird', 'boat', 'book', 'bottle', 'building', 'bus',
               'cabinet', 'car', 'cat', 'ceiling', 'chair', 'cloth',
               'computer', 'cow', 'cup', 'curtain', 'dog', 'door', 'fence',
               'floor', 'flower', 'food', 'grass', 'ground', 'horse',
               'keyboard', 'light', 'motorbike', 'mountain', 'mouse', 'person',
               'plate', 'platform', 'pottedplant', 'road', 'rock', 'sheep',
               'shelves', 'sidewalk', 'sign', 'sky', 'snow', 'sofa', 'table',
               'track', 'train', 'tree', 'truck', 'tvmonitor', 'wall', 'water',
               'window', 'wood')

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default='demo/source/test.png', help='source')
    parser.add_argument('--obj_class', type=str, default='wall', help='class to segment')
    parser.add_argument('--config', type=str, default='models/pspnet_r101-d8_480x480_80k_pascal_context_59.py', help='model\'s config')
    parser.add_argument('--chkpt', type=str, default='models/pspnet_r101-d8_480x480_80k_pascal_context_59_20210416_114418-fa6caaa2.pth', help='model\'s checkpoint')
    parser.add_argument('--output', type=str, default='demo/mask/test.png', help='mask path')
    parser.add_argument('--device', type=str, default='cpu', help='device to run model on (cpu, cuda)')
    return parser

if __name__ == '__main__':
        
    opt =  make_parser().parse_args()
    config_file = opt.config
    checkpoint_file = opt.chkpt
    
    img = opt.image
    
    id_select = None
    for idx, value in enumerate(CLASSES):
        if value == opt.obj_class:
            id_select = idx-1
    if id_select:
        # build the model from a config file and a checkpoint file
        model = init_segmentor(config_file, checkpoint_file, device=opt.device)

        # test a single image and show the results
        result = inference_segmentor(model, img)
        res = np.array(result[0])
        res[res !=id_select] = 0
        res[res == id_select] = 1
        cv2.imwrite(opt.output, res)
    else:
        print(f'obj {opt.obj_class} wasn\'t not found')
