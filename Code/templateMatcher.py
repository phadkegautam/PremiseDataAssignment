# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 05:16:49 2021

@author: Gautam
"""


import MTM

from MTM import matchTemplates, drawBoxesOnRGB
from MTM.NMS import NMS
import pandas as pd

import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
from os import walk

def template_matcher(template_image_path, csvFile_data_path, image_path, keep_image,
                     text_detected_threshold, text_not_detected_threshold):
    """
    Params:
        template_image_path ---> Path to the template logos
        csvFile_data_path ---> Path to the csv data file
        image_path ---> Path to input images
        keep_image ---> type = dict. Decide whether to accept the image based on text only
        text_detected_threshold ---> float between 0 and 1
        text_not_detected_threshold ---> float between 0 and 1
    """
    
    image_path = []
    for(dirpath, dirnames, filenames) in walk(template_image_path):
        image_path.extend(filenames)
        
    templates = []
    for i in range(len(filenames)):
        sample = cv2.imread(template_image_path + filenames[i])
        templates.append(sample)
    
    templates = np.array(templates)
        
    dataset = pd.read_csv(csvFile_data_path)
    
    for key in keep_image.keys():
        hit_flag = False
        temp_key = key.split("/")[-1]
        
        for i in range(len(templates)):
            test_image_temp = cv2.imread(image_path + temp_key)
    
            listTemplate = [('template_image', templates[i])]
    
            if(keep_image[key][0] == "yes"):
                Hits = matchTemplates(listTemplate, test_image_temp, N_object=10,score_threshold=text_detected_threshold, method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.3)
                if(len(Hits) > 0):
                    hit_flag = True
                    break
            
            elif(keep_image[key][0] == "no"):
                Hits = matchTemplates(listTemplate, test_image_temp, N_object=10,score_threshold=text_detected_threshold, method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.3)
                if(len(Hits) > 0):
                    hit_flag = True
                    break
        
        if(hit_flag):
            keep_image[key].append("yes")
        elif(not hit_flag):
            keep_image[key].append("no")
            
    return keep_image
            
        
        
    
    
    
    
    
    
    
    
        
    
        