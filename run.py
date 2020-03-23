#import asyncio
import matplotlib.pyplot as plt
import json
import os, sys
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from PIL import Image
#폐렴 분류 모델
# from semi_model import SemiModel

import cv2

from flask_cors import CORS,cross_origin


#from functools import partial
#from werkzeug import secure_filename

app = Flask(__name__)

#이미지 폴더 경로
IMG_FOLDER = os.path.join(os.path.join('static', 'img'),'upload_img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

#폐렴 분류 모델 로딩
# PredictModel = SemiModel('v3_10-0.2601.hdf5')


cors = CORS(app, allow_headers='Content-Type', CORS_SEND_WILDCARD=True)

@app.route('/upload')
def render_file():
   return render_template('upload.html')

@app.route('/')
def main_page():
  return render_template('index.html')

@app.route('/result')
def result_page():
  return render_template('result.html')


@app.route('/cam2', methods=['POST'])
def send_cam2():
  type = "two"
  json_data = request.get_json()
  # print("### cam ####",json_data)
  full_filename = json_data['img_path']

  if type=="two":
    # predict_cam_using_path
     print("d")
  elif type == "one":  
    
    #cv2Image = numpy data
    cv2Image = cv2.imread(full_filename)
    # cv2Image = PredictModel.cam(full_filename)
    # print("#### cv2Image : ",cv2Image)
    img = Image.fromarray(cv2Image.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})




@app.route('/cam', methods=['POST'])
@cross_origin(origins='*', send_wildcard=True)
def send_cam():
  json_data = request.get_json()
  # print("### cam ####",json_data)
  full_filename = json_data['img_path']

  # prepare headers for http request
  content_type = 'image/jpeg'
  headers = {'content-type': content_type}

  #cv2Image = numpy data
  cv2Image = cv2.imread(full_filename)
  # print("#### cv2Image : ",cv2Image)

  # encode image as jpeg
  # _, img_encoded = cv2.imencode('.jpg', cv2Image)
  # print("#### img_encoded : ",img_encoded)
  # send http request with image and receive response
  # img_encodedStr=img_encoded.tostring()

  # data = cv2.imencode('.png', cv2Image)[1].tobytes()

  # response_img = requests.post(test_url, data=img_encodedStr, headers=headers)
  # return response_img;

  # data = cv2.imencode('.png', cv2Image)[1].tobytes()
  # data = cv2.imencode('.jpg', cv2Image)[1].tobytes()
  # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
  # print("#### img_encodedStr : ",img_encodedStr)
  # b64=base64.encodestring(img_encodedStr)

  #response json
  # return jsonify(hello='world')


#이미지 서버에 저장 후 result page에 노출하기
@app.route('/imgs',methods=['POST'])
def upload_imgs():
  if request.method == 'POST':

    #img = request.files['files']
    imgs = request.files.getlist("file[]")
    # imgs = request.files.to_dict()
    # print("imgs : ",imgs)
    #이미지가 저장된 전체 경로
    resultDataList = []

    for img in imgs:
      # print("img : ",img)
      # print("filename : ",img.filename)
      #저장할 경로 + 파일명
      full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
      full_filename = full_filename.replace('\\','/')
      img.save(full_filename)

      # 모델 없이 테스트 용
      prob = 0.984324

      # 배포 용(모델 적용)
      # prob = PredictModel.predict_using_path(full_filename)
      # result_set = PredictModel.predict_cam_using_path(full_filename)
      # prob=result_set["prob"]
      # superimposed_img=result_set["superimposed_img"]
      #cam 테스트용
      superimposed_img = cv2.imread(full_filename)
      #print("#결과 : ",prob)

      #폐렴의심 여부 (1이면 폐렴, 0이면 정상)
      isPneumonia = 1 if prob > 0.5 else 0
      #폐렴검출 정확도
      acc = int(prob*100)

      #cam 결과 이미지 base64로 변환
      img = Image.fromarray(superimposed_img.astype("uint8"))
      rawBytes = io.BytesIO()
      img.save(rawBytes, "JPEG")
      rawBytes.seek(0)
      img_base64 = base64.b64encode(rawBytes.read())
      #응답할 결과 데이터
      resultDataList.append({'img_path' : full_filename,
                   'acc' : acc, 'isPneumonia' : isPneumonia, 'cam_img':str(img_base64)})
      
      # return jsonify({'status':str(img_base64)})
    # print("### resultDataList : ", resultDataList)

    return render_template("result.html", resultDataList = resultDataList)

@app.route('/text', methods=['GET','POST'])
def upload_text():
  if request.method =='POST':
    req = request.form
    name = req.get('name')
    # print("name : "+name)

    return redirect("/", name = name)
   
if __name__ == '__main__':
    #서버 실행
   app.run(debug = True)
  #  app.run(host='0.0.0.0')
