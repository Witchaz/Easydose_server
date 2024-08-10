import pytesseract,os
from flask import Flask,request,template_rendered
from PIL import Image

app = Flask(__name__)

current_path = os.getcwd()
abs_path = os.path.join(current_path,"Tesseract-OCR","tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = abs_path
@app.route('/')
def home():    
    return template_rendered.render('home.html')

@app.route('/ocr',methods=['POST'])
def ocr():
    try:
        imageFile = request.files.get('imagefile','')
        result = pytesseract.image_to_string(imageFile,lang="tha+eng")
        return result
    except FileExistsError as exception:
        return "Invalid file"
    except Exception as e:
        return str(e) 

if __name__ =="__main__":
    app.run(debug=True)