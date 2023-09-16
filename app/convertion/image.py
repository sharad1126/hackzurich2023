from PIL import Image

import pytesseract

import os

# If you don't have tesseract executable in your PATH, include the following:
# Link to install it: https://tesseract-ocr.github.io/tessdoc/Installation.html
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

#get the current directory
cdir = os.getcwd() 
#get the parent directory
pdir = os.path.dirname(cdir)
#print("Current Directory: ", cdir) 
#print("Parent Directory: ", os.path.dirname(cdir))
# assign directory
directory = os.path.join(pdir,'files')
#print(directory)
 
# iterate over files in
# that directory

for filename in os.listdir(directory):
    #get the filepath
    f = os.path.join(directory, filename)
    #split the filname and the extension
    filename_stripped, extension = os.path.splitext(filename)
    #print(filename_stripped)
    #print(extension)
    #if f.suffix == ".png" or ".jpg":
    #only work with it, if it is a picture
    if extension == ".png" or extension == ".jpg":
        #convert image to text
        text_from_image = pytesseract.image_to_string(Image.open(f))
        #join the paths, to the place where new files should be stored
        image_text_path = directory + "\\" + filename_stripped + ".txt"
        #print(image_text_path)
        #create the new file
        t = open(image_text_path, "w+")
        #write in the new file
        t.write(text_from_image)
        #close the file
        t.close()

