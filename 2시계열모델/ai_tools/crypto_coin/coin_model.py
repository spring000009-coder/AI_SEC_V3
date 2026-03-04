import tensorflow as tf
import numpy as np
import pickle
import os
import requests
from datetime import datetime, timedelta
import sklearn

# print(os.getcwd())#D:\infor_sec_service
# print(os.path.abspath(__file__))
ROOT_PATH = os.getcwd()
CURR_PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-1])
model = None
rbs_scaler = None
time_step = 90
target_list = ["opening_price", "high_price", "low_price", "trade_price", \
               "prev_closing_price", "change_rate"]

if os.path.exists(CURR_PATH + "/BTC_90_lstm.keras"):
    model = tf.keras.models.load_model(CURR_PATH + "/BTC_90_lstm.keras")
    if model:
        print("모델 불러오기 성공")
    else:
        print("모델 불어오기 실패")
else:
    print("path fail")

if os.path.exists(CURR_PATH + "/config/BTC_rbs.pre"):
    with open(CURR_PATH + "/config/BTC_rbs.pre", "rb") as fp:
        rbs_scaler = pickle.load(fp)
    if rbs_scaler:
        print("스케일러 불러오기 성공")
    else:
        print("스케일러 불어오기 실패")
else:
    print("path fail")


# ======= utils start
def extract_data(raw_datas):  # 상관성에 따른 데이터 추출
    global target_list
    conv_datas = []
    for unit in raw_datas:
        temp = []
        for key in unit:
            if key in target_list:
                temp.append(unit[key])
        if temp:
            conv_datas.append(temp)
    print(len(conv_datas))
    return conv_datas


# ======== utils end

def get_datas(coin_name, receive_count=200):  # 1. 빗썸으로 부터 오늘 날짜 데이터 받아오기
    # 오늘 날짜
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #2026-02-06 01:11:28.126344
    cur_time = datetime.now()
    count = 200
    # date_str = "2026-02-06 00:00:01"#"yyyy-MM-dd HH:mm:ss"
    date_str = ""
    time_cnt = receive_count // count
    if receive_count % count:
        time_cnt += 1
    ret_datas = []
    for c in range(time_cnt):
        date_str = cur_time.strftime("%Y-%m-%d %H:%M:%S")
        # 7-21 '2025-07-22T00:00:00',  '2025-01-03T00:00:00'
        # 2-6 '2026-02-06T00:00:00      '2025-07-21T00:00:00'
        # print("pre ",cur_time)
        cur_time = cur_time - timedelta(days=count)
        # print("aft ",cur_time)
        DAY_CANDLE = r"https://api.bithumb.com/v1/candles/days?market=KRW-{}&count={}&to={}" \
            .format(coin_name, count, date_str)
        receive_data = (requests.get(DAY_CANDLE).json())
        receive_data.reverse()  # 시간 순서 오름차순으로 뒤집기
        ret_datas = receive_data + ret_datas
    raw_datas = extract_data(ret_datas)
    return raw_datas  # [{},{},{},.......]


def preprocessing_datas(tar_datas):  # 2. 데이터 스케일링 전처리
    global rbs_scaler
    print("tar shape", np.array(tar_datas).shape)
    return rbs_scaler.transform(tar_datas)


def create_datas(raw_datas):  # 3. 시계열 x데이터 생성부
    global time_step
    print("x데이터생성부:", raw_datas.shape)
    # x데이터생성부: (200, 6)
    return np.array([raw_datas[-time_step:]])


def predict_datas(x_datas, day_cnt=1):  # 예측데이터 생성
    y_pred_datas = []
    for c in range(day_cnt):
        tmp_pred = model.predict(x_datas)
        y_pred_datas.append(tmp_pred[0])
        # 기존 데이터의 0번 제거 후 마지막에 현재 예측값을 삽입
        x_datas = np.delete(x_datas, 0, axis=1)  # 맨앞의 데이터 삭제
        x_datas = np.append(x_datas, np.array([tmp_pred]), axis=1)  # 마지막 데이터 예측값으로 추가
        # 마지막 데이터 동일 여부 검증
        # print(tmp_pred)
        # print(x_datas[-1,-1,:])
        # print(x_datas.shape)
    # numpy 타입은 웹에서 리턴시 오류 발생하므로 기본타입 리스트로 변경후 리턴
    return np.array(y_pred_datas)


def convt_data(tar_ydatas):  # 예측데이터 가격 복원
    conv_price = rbs_scaler.inverse_transform(tar_ydatas)
    return {"label": target_list, "pred_info": conv_price.tolist()}