# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:26:34 2021

@author: Gautam
"""


import argparse
from templateMatcher import template_matcher
from textExtraction import text_extraction_ocr
from textCleaner import text_cleaner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type = str, required = True,
                        help = 'Specify the path to the image files')
    parser.add_argument('--csvFile_data_path', type = str, required = True,
                        help = 'Specify the path to the metadeta')
    parser.add_argument('--template_image_path', type = str, 
                        help = 'Provide the logo path if it exists')
    parser.add_argumet('--gpu', type = str, default = False,
                       help = "True if GPU support is needed")
    parser.add_argument('--farma_threshold', type = float, default = 0.3,
                        help = "Use the word farmacia")
    parser.add_argument('--word_threshold', type = float, default = 0.4,
                        help = "Select words about this probability threshold")
    parser.add_argument('--levenshtein_threshold', type = float, default = 0.4,
                        help = "Select words below this distance value")
    parser.add_argument('--text_detected_threshold', type = float, default = 0.3,
                        help = "Use this for text extracted from OCR")
    parser.add_argument('--text_not_detected_threshold', type = float, default = 0.6,
                        help = "Use this if text cannot be detected")
    
    args = parser.parse_args()
    
    image_path = args.image_path
    csvFile_data_path = args.csvFile_data_path
    template_image_path = args.template_image_path
    gpu = args.gpu
    farma_threshold = args.farma_threshold
    word_threshold = args.word_threshold
    levenshtein_threshold = args.levenshtein_threshold
    text_detected_threshold = args.text_detected_threshold
    text_not_detected_threshold = args.text_not_detected_threshold
    
    final_result_dict = text_extraction_ocr(image_path, csvFile_data_path, gpu)
    keep_image = text_cleaner(final_result_dict, csvFile_data_path, farma_threshold, word_threshold, levenshtein_threshold)
    keep_image = template_matcher(template_image_path, csvFile_data_path, image_path, keep_image,
                     text_detected_threshold, text_not_detected_threshold)
    
    print(keep_image)
    
    
    