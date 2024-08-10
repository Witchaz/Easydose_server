import os,base64
from flask import Flask,request,template_rendered
from PIL import Image
import os
from numpy import random
from collections import Counter
from google.cloud import vision
from PIL import Image

app = Flask(__name__)

def detect_text(content):
    """Detects text in the file."""
    from google.cloud import vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/app/vision_key.json"
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    ans = ""
    for text in texts:
        ans += text.description

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return ans

@app.route('/')
def home():    
    return "Hello world!"

@app.route('/ocr',methods=['POST'])
def ocr():
    try:
        data = request.json.get('image_base64', '')

        # แปลง base64 string กลับเป็น binary
        image_data = base64.b64decode(data)
        # เรียกใช้ฟังก์ชัน OCR
        result = detect_text(image_data)
        return result
    except FileExistsError as exception:
        return "Invalid file"
    # except Exception as e:
    #     return str(e) 

if __name__ =="__main__":
    app.run(debug=True)

