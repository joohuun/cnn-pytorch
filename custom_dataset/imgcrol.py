import os
import shutil
from bing_image_downloader import downloader  # 크롤링용

mat.rcParams['font.family'] = 'Gulim'

directory_list = [
    './custom_dataset/train/',
    './custom_dataset/test/',
]

# 초기 디렉토리 만들기
for directory in directory_list:
    if not os.path.isdir(directory):
        os.makedirs(directory)


# 수집한 이미지를 학습 데이터와 평가 데이터로 구분하는 함수
def dataset_split(query, train_cnt):
    # 학습 및 평가 데이터셋 디렉토리 만들기
    for directory in directory_list:
        if not os.path.isdir(directory + '/' + query):
            os.makedirs(directory + '/' + query)
    # 학습 및 평가 데이터셋 준비하기
    cnt = 0
    for file_name in os.listdir(query):
        if cnt < train_cnt:
            print(f'[Train Dataset] {file_name}')
            shutil.move(query + '/' + file_name,
                        './custom_dataset/train/' + query + '/' + file_name)
        else:
            print(f'[Test Dataset] {file_name}')
            shutil.move(query + '/' + file_name,
                        './custom_dataset/test/' + query + '/' + file_name)
        cnt += 1
    shutil.rmtree(query)


###########################################################################################
## 이미지 파일 크롤링 해두는 부분입니다. 주석 풀어서 쓰시면되고 한번 크롤링 후에는 다시 주석처리 ~~
###########################################################################################

# list = ['신동엽', '정상훈', '안영미', '김민교', '권혁수', '정이랑', '정혁', '주현영', '이소진', '솔빈']
list = ['신동엽', '정상훈', '안영미', '김민교', 'snl권혁수', 'snl정이랑', 'snl정혁', '주현영', 'snl이소진', 'snl솔빈']

for name in list:
  query = name #검색 단어
  # bing.com에서 이미지 다운로드
  downloader.download(query, limit=108,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=60)
  # output_dir : 현재 디렉토리에 '마동석'이란 폴더 만들어
  # 위 2)함수 불러와서 수집한 이미지 학습 데이터와 평가데이터로 구분
  dataset_split(query, 72)
