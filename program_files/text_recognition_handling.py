import image_preprocessing_handling as iph
import pytesseract
import json
import re
from PIL import Image

def get_card_description(filename,angle=0):
    descriptions = []
    iph.preprocess_images_all_versions(filename,angle)
    image = Image.open("temp/preprocessed_card_120.jpg")
    descriptions.append(pytesseract.image_to_string(image))
    image = Image.open("temp/preprocessed_card_145.jpg")
    descriptions.append(pytesseract.image_to_string(image))
    image = Image.open("temp/preprocessed_card_170.jpg")
    descriptions.append(pytesseract.image_to_string(image))
    return descriptions

def get_definitions(filename,angle=0):
    definitions_to_display = ""
    regex = re.compile('[^a-zA-Z ]')
    words = []
    card_descriptions = get_card_description(filename,angle)
    for description in card_descriptions:
        description = description.lower()
        description = description.replace('\n',' ')
        description = regex.sub('',description)
        words_part = description.split()
        for word in words_part:
            if word not in words:
                words.append(word)
    keyword_dictionary = None
    with open('program_files/resources/dictionary.json','r') as keyword_dict:
        keyword_dictionary = json.load(keyword_dict)
    for word in words:
        try:
            found_content = keyword_dictionary[word]
            part = word + ' - ' + found_content + '\n'
            definitions_to_display += part
        except:
            pass
    return definitions_to_display