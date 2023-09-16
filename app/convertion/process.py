#import zipfile module
from zipfile import ZipFile
from PIL import Image
import pytesseract
import os
import shutil
import xml.etree.ElementTree as ET
from lxml import etree
import re


# Define your regular expression patterns
patterns = {
    'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}\b',
    'PHONE': r'(?:(?:+\d{1,3}[-.\s]?)?(?\d{3})?[-.\s]?\d{3}[-.\s]?\d{4})',
    'IBAN': r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b',
    'GENDER': r'\b(male|female)\b',
    'RSA_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----'
    }

#with ZipFile('filename.zip', 'r') as f:

    #extract in current directory
    #f.extractall()

# If you don't have tesseract executable in your PATH, include the following:
# Link to install it: https://tesseract-ocr.github.io/tessdoc/Installation.html
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

#get the current directory
cdir = os.getcwd() 
#get the parent directory
pdir = os.path.dirname(cdir)
# assign directory
directory = os.path.join(pdir,'files')

#make new folder for processed files
processed_directory_path = directory + "\\" + 'processed'
if os.path.isdir(processed_directory_path) == True:
    shutil.rmtree(processed_directory_path)
    processed_directory = os.mkdir(processed_directory_path)
else:
    processed_directory = os.mkdir(processed_directory_path)

# iterate over files in that directory
for filename in os.listdir(directory):
    #get the filepath
    f = os.path.join(directory, filename)
    #print(f)
    #split the filname and the extension
    filename_stripped, extension = os.path.splitext(filename)
    if extension == ".zip":
        with ZipFile(f, 'r') as z:
            #extract in current directory
            try: 
                #has to be changed so that it is not in a folder
                z.extractall(processed_directory_path + "\\" + filename)
                #z.extractall()
            except: 
                print("fail") #here we should flag, since it is encrypted
    

    #only work with it, if it is a picture
    elif extension == ".png" or extension == ".jpg":
        #convert image to text
        text_from_image = pytesseract.image_to_string(Image.open(f))
        #join the paths, to the place where new files should be stored
        image_text_path = processed_directory_path + "\\" + filename_stripped + ".txt"
        #print(image_text_path)
        #create the new file
        t = open(image_text_path, "w+")
        #write in the new file
        t.write(text_from_image)
        #close the file
        t.close()

    #moving the txt did not work
    elif extension ==".txt":
        #os.rename(f, processed_directory_path + "\\" + filename)
        newpath = processed_directory_path + "\\" + filename
        #old_text = open(f, "r")
        #print(old_text)
        with open(f, 'r', encoding='unicode_escape', errors='replace') as source_file:
            # Read the content of the source file
            content = source_file.read()

        # Open the target file for writing (this will create the file if it doesn't exist)
        with open(newpath, 'w+', encoding='UTF-8') as target_file:
            # Write the content to the target file
            target_file.write(content)
        #create the new file
        #t = open(newpath, "w+")
        #write in the new file
        #t.write(old_text)
        #close the file
        #t.close()
        #old_text.close"""
    elif extension == ".xml":
        #parse the xml
        #root = ET.fromstring(country_data_as_string)
        #to make the parsing more efficient (incremental): https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.XMLPullParser.read_events
        parser = etree.XMLParser(recover=True)
        with open(f, 'r', encoding='unicode_escape') as file:
            xml_content = file.read()
        #tree = ET.parse(xml_content, parser=parser)
        #root = tree.getroot()
        root = ET.fromstring(xml_content)
        #print(root.tag)
        #for child in root:
            #print(child.tag, child.attrib)
        # Define a recursive function to traverse the XML tree
        def traverse_element(element, level=0):
            # Print the element's tag and attributes
            #print('  ' * level + f"Tag: {element.tag}, Attributes: {element.attrib}")
            
            # Print the text content of the element, if it exists
            if element.text:
                print('  ' * level + f"Text: {element.text.strip()}")
                

                # Match and print patterns in the text content
                for pattern_name, pattern in patterns.items():
                    if any(char.isalnum() for char in element.text):
                        matches = re.findall(pattern, element.text)
                        if matches:
                            print('  ' * level + f"Pattern '{pattern_name}' Matches: {matches}")
    
            
            # Recursively traverse child elements
            for child in element:
                traverse_element(child, level + 1)

        # Start traversal from the root element
        traverse_element(root)


