import os
import pickle
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
ROOT_PATH = os.getcwd()
CURR_PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-1])
print(ROOT_PATH)
print(CURR_PATH)
latent_dim=100
APP_PATH = "\\".join(ROOT_PATH.split("\\")[:2])
#CURR_PATH+"/generator.keras"
if os.path.exists(CURR_PATH+"/generater.keras"):
    #quntization_config 오류시 파일 zip 변걍후
    # config.json 파일에서 해당 항목 삭제
    gener = tf.keras.models.load_model(
        CURR_PATH+"/generater.keras")
#이미지 생성
def gener_print(noise):
  global gener
  plt.figure(figsize=(5,5))
  res = gener.predict(noise,verbose=0)
  res[0]=255-res[0]
  plt.imshow(res[0],cmap="gray")
  plt.xticks([])
  plt.yticks([])
  now = datetime.now()
  fname = now.strftime("%Y.%m.%d.%H_%M.%S.png")
  plt.savefig(f"{APP_PATH}/static/images/user_img/{fname}")
  return f"images/user_img/{fname}"
def create_noise(loc=0.0,scale=1.0,user_noise=None):
    #사용자가 업로드 이미지는 50,50 tkdlwm djqfhem rksmdgkr
    # 미구현함(1, 믈라이언드락 서버로 이미지 업로두 코드를 작성
    # 2. 업로드된 이미지르 불러와서 변결
    global latent_dim
    if not user_noise:
        user_noise = np.random.normal(
            loc=loc,scale=scale, size=(1, latent_dim))
    return gener_print(user_noise)


