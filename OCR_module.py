from pathlib import Path
import pytesseract
from PIL import Image
import os

current_path = os.getcwd()
tesseract_path = "\\Tesseract-OCR\\tesseract.exe"
abs_path = os.path.join(current_path,"Tesseract-OCR","tesseract.exe")
print(current_path)
print(abs_path)


pytesseract.pytesseract.tesseract_cmd = Path(abs_path)

print(pytesseract.image_to_string(Image.open('test_image.jpg'),lang="tha"))

class ocr_module:
    def __init__(self):
        print(pytesseract.image_to_string(Image.open('test_image.jpg')))
        
        