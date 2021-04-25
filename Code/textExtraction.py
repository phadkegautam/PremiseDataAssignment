# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 02:32:12 2021

@author: Gautam
"""


import torch
import cv2
import easyocr

import matplotlib.pyplot as plt
import pandas as pd

def text_extraction_ocr(image_path, csvFile_data_path, gpu):
    
    """
    Params:
        image_path --> Path to the Pharmacy images
        csvFile_data_path --> Path to the csv data file
        gpu --> type = bool. Specify whether gpu is needed or not
    """
    
    #Populate path to all the images
    dataset = pd.read_csv(csvFile_data_path)
    photo_id = dataset['photo']
    photo_id = photo_id.str.split("/")
    
    file_paths = []
    for i in range(len(photo_id)):
        file_paths.append(image_path + photo_id[i][1])
        
    #Create OCR Reader Object
    reader = easyocr.Reader(['en'], gpu = gpu)
    result_dict = dict()
    for i in range(len(file_paths)):
        temp = reader.readtext(file_paths[i])
        result_dict[file_paths[i]] = temp
        
    final_result_dict = dict()
    for keys in result_dict.keys():
        temp_key = keys.split("/")
        temp_key = temp_key[-2] + "/" + temp_key[-1]
        final_result_dict[temp_key] = result_dict[keys]
        
    return final_result_dict

    


        
    
    
    
    