import cv2
import numpy as np
import argparse
import os
from glob import glob

class PatternApply():
    '''
    Class for Applying Selected Pattern onto the object
    '''
    def __init__(self, pattern_path, mask_path, output_path) -> None:
        self.pattern_png = cv2.imread(pattern_path) # pattern
        self.corners = [] # selected corners to project onto
        
        self.seg_png = cv2.imread(mask_path) # read the segmentation mask of the scene
        
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok = True)
        self.img_ = None # img to show
        
    def apply(self, img):
        H, W, _ = self.pattern_png.shape
        pts1 = np.float32([[0, 0], [W, 0],
                       [W, H], [0, H]])
        pts2 = np.float32(self.corners)
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(self.pattern_png, matrix, img.shape[:2][::-1])
        
        result *= self.seg_png # pick only parts covering the selected class id (ex., bed, walls)
        img[result != 0] = img[result != 0]*0.2 + result[result != 0]*0.8
        self.img_ = img
        
    def save_img(self,):
        imgs = glob(os.path.join(self.output_path, "*.png")) + glob(os.path.join(self.output_path, "*.jpg"))
        cv2.imwrite(os.path.join(self.output_path, f"{len(imgs)}.png"), img)
        
    def getImg(self):
        return self.img_
    
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        pattern.corners.append([x,y])
        # displaying the coordinates
        # on the image window
        img_show = img.copy()
        img_show = cv2.circle(img_show, (x, y), 2, (0,0,0))
        cv2.imshow('image', img_show)
        
    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN: # remove
        pattern.corners = pattern.corners[:-1]
        cv2.imshow('image', img)
    
    # click middle button to apply pattern    
    if event==cv2.EVENT_MBUTTONDOWN and len(pattern.corners) == 4:
        pattern.apply(img)
        pattern.corners = []
        cv2.imshow('image', pattern.getImg())

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default='demo/source/test.png', help='source')
    parser.add_argument('--pattern', type=str, default='demo/patterns/mramor.jpg', help='pattern path')
    parser.add_argument('--mask', type=str, default='demo/mask/test.png', help='mask path')
    parser.add_argument('--output', type=str, default='demo/results/', help='result path')
    return parser

if __name__=="__main__":
    opt =  make_parser().parse_args()
    pattern = PatternApply(opt.pattern, opt.mask, opt.output)
    
    # reading the image
    img = cv2.imread(opt.image)
  
    # displaying the image
    cv2.imshow('image', img)
    
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    
    # Save final img
    pattern.save_img()
    
    # close the window
    cv2.destroyAllWindows()