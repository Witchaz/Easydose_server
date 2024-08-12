import os,base64
from flask import Flask,request
import google.generativeai as genai
from google.cloud import vision


app = Flask(__name__)

os.environ["API_KEY"] = "AIzaSyCW6lXrGtIbxu4eAa5VXOsIGHv41cm-7MQ"
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash',generation_config={
    "max_output_tokens":500
})

def detect_text(content):
    """Detects text in the file."""
    # from google.cloud import vision
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'
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
        data = detect_text(image_data)
        question = f"\nเราจะถามคำถามจากข้อมูลที่ให้ไปตอบให้กระชับที่สุด\n1)ยาตัวนี้มีชื่อว่าอะไร\n2)ยาตัวนี้ต้องกี่เวลาไหน\n3)ยาตัวนี้กินครั้งละกี่เม็ด"
        result = model.generate_content(data+question)
        response = {
            "text": result.text
        }
        return response
    except FileExistsError as exception:
        response = {
            "text": "Invalid file"
        }
        return response
    except Exception as e:
        response = {
            "text": str(e)
        }
        return response

if __name__ =="__main__":
    app.run(host="0.0.0.0", debug=True)

