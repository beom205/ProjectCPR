#import asyncio
import matplotlib.pyplot as plt
import json
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
#폐렴 분류 모델
#from semi_model import SemiModel
#from functools import partial
#from werkzeug import secure_filename

app = Flask(__name__)

#이미지 폴더 경로
IMG_FOLDER = os.path.join(os.path.join('static', 'img'),'upload_img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

#폐렴 분류 모델 로딩
#PredictModel = SemiModel('v3_10-0.2601.hdf5')

@app.route('/upload2')
def render_file():
   return render_template('upload.html')

@app.route('/')
def main_page():
  return render_template('index.html')

#이미지 서버에 저장 후 result page에 노출하기
@app.route('/imgs',methods=['GET','POST'])
def upload_imgs():
  if request.method == 'POST':

    #img = request.files['files']
    imgs = request.files.getlist("file[]")
    # imgs = request.files.to_dict()
    print("imgs : ",imgs)
    #이미지가 저장된 전체 경로
    resultDataList = []

    for img in imgs:
      # print("img : ",img)
      # print("filename : ",img.filename)
      #저장할 경로 + 파일명
      full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
      full_filename = full_filename.replace('\\','/')
      img.save(full_filename)

      #모델 없이 테스트 용
      prob = 0.984324
      #print("#결과 : ",prob)
      #폐렴의심 여부 (1이면 폐렴, 0이면 정상)
      isPneumonia = 1 if prob > 0.5 else 0
      #폐렴검출 정확도
      acc = int(prob*100)
      #응답할 결과 데이터
      resultDataList.append({'imgs' : full_filename,
                   'acc' : acc, 'isPneumonia' : isPneumonia})

    print("### resultDataList : ", resultDataList)

    return render_template("result3.html", resultDataList = resultDataList)

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
   #app.run(host='0.0.0.0')
