# Classify Pneumonia with Resnet50



### 브랜치 설명 <br>
* master : 배포용 버전 적용 브랜치(현재 개발완료한 v2 적용)
* v1 : version 1, 1개의 사진만 분석
* v2 : version 2, 사진 여러장 동시 분석, 결과별 표시, 실제 배포판
* v2_server : 테스트 서버용(예측모델 미적용 버전, 예측모델 적용하면 keras, tf 없으면 flask 서버가 작동하지 않기 때문에 Client 화면 테스트를 위해 예측모델 미적용함)
* v2_server_deep : 배포 서버 테스트용(예측모델 적용 버전)
* v2_front : 테스트 서버용 프론트 수정 브랜치(예측모델 미적용) 
* Deeplearning : 딥러닝 모델 개발용 브랜치
* v3 : cam 결과 표시 버전(개발중)
