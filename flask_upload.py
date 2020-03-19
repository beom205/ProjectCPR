#import asyncio
import matplotlib.pyplot as plt
import json
from flask import Flask, render_template, request, redirect, url_for
import os
#from functools import partial
#from werkzeug import secure_filename

app = Flask(__name__)

IMG_FOLDER = os.path.join(os.path.join('static', 'img'),'upload_img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route('/upload2')
def render_file():
   return render_template('upload.html')

@app.route('/')
def main_page():
  return render_template('index.html')

@app.route('/result')
def result_page():
  return render_template('result3.html')


#이미지 서버에 저장 후 result page에 노출하기
@app.route('/imgs',methods=['GET','POST'])
def upload_imgs():
  if request.method == 'POST':
    img = request.files['file']
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    img.save(full_filename)

    #저장할 경로 + 파일명
    return render_template("result3.html", imgs = full_filename)

@app.route('/text', methods=['GET','POST'])
def upload_text():
  if request.method =='POST':
    req = request.form
    name = req.get('name')
    print("name : "+name)

    return redirect("/", name = name)
   
if __name__ == '__main__':
    #서버 실행
   app.run(debug = True)