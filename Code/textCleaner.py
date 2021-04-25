# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 04:46:32 2021

@author: Gautam
"""
from similarity.normalized_levenshtein import NormalizedLevenshtein
import pandas as pd


def append_farmacia(test_name, farma_threshold):
    normalized_levenshtein = NormalizedLevenshtein()
    farmacia_flag = False
    for i in range(len(test_name)):
        if(normalized_levenshtein.distance("farmacias", test_name[i].lower()) < farma_threshold):
            farmacia_flag = True
      
    if(not farmacia_flag):
        test_name.append("farmacias")
      
    return test_name

def clean_results(test_image, word_threshold):
    
    clean_result = []
    for i in range(len(test_image)):
        if(test_image[i][2] > word_threshold):
            test_image[i] = list(test_image[i])
            test_image[i][1] = test_image[i][1].strip().split(" ")
            clean_result.append(test_image[i])
            
    return clean_result

def filter_results(clean_result, test_image, levenshtein_threshold):
    normalized_levenshtein = NormalizedLevenshtein()
    final_result = []
    for i in range(len(clean_result)):
        append_flag = True
        for j in range(len(clean_result[i][1])):
            for k in range(len(test_image)):
                if(normalized_levenshtein.distance(clean_result[i][1][j].lower(), test_image[k].lower()) <= levenshtein_threshold):
                    clean_result[i][1] = " ".join(clean_result[i][1])
                    final_result.append(tuple(clean_result[i]))
                    append_flag = False
                    break
            if(append_flag == False):
                break

def text_cleaner(final_result_dict, csvFile_data_path, farma_threshold, word_threshold, levenshtein_threshold):
    
    """
    Params:
        final_result_dict ---> Output dict from OCR API
        csvFile_data_path ---> Path to the csv data file
        farma_threshold ---> Whether to include the word farmacy or not
        word_threshold ---> Threshold value to include the given word
        levenshtein_threshold ---> Acceptable distance between two words
    """
    
    #Populate path to all the images
    dataset = pd.read_csv(csvFile_data_path)
    photo_name = dataset[['photo','name']]
    
    
    keep_image = dict()
    
    for idx in range(len(photo_name.photo)):
        keep_image.setdefault(photo_name.photo[idx], list())
        test_image = final_result_dict[photo_name.photo[idx]].copy()
        test_name = photo_name.name[idx]
        test_name = test_name.strip().split(" ")
        
        test_name = append_farmacia(test_name, farma_threshold)
        clean_result = clean_results(test_image, word_threshold)
        final_result = filter_results(clean_result, test_image, levenshtein_threshold)
        
        if(len(final_result) == 0):
            keep_image[photo_name.photo[idx]].append("no")
        elif(len(final_result) >= 0):
            keep_image[photo_name.photo[idx]].append("yes")
            
        keep_image[photo_name.photo[idx]].append(final_result)
        
    return keep_image
        
        
        
        
        
        