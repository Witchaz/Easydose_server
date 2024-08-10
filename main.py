import pytesseract,os
from flask import Flask,request,template_rendered
from PIL import Image
import os
from numpy import random
from collections import Counter
from google.cloud import vision
from PIL import Image
\

app = Flask(__name__)

# current_path = os.getcwd()
# abs_path = os.path.join(current_path,"Tesseract-OCR","tesseract.exe")
# pytesseract.pytesseract.tesseract_cmd = abs_path

def detect_text(content):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    # with open(path, "rb") as image_file:
    #     content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')


    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

@app.route('/')
def home():    
    return template_rendered.render('home.html')

@app.route('/ocr',methods=['POST'])
def ocr():
    try:
        imageFile = request.files.get('imagefile','')
        # result = pytesseract.image_to_string(imageFile,lang="tha+eng")
        result = detect_text(imageFile)
        return result
    except FileExistsError as exception:
        return "Invalid file"
    except Exception as e:
        return str(e) 

if __name__ =="__main__":
    app.run(debug=True)

