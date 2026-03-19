import os
import pickle
import tensorflow as tf
import numpy as np
ROOT_PATH = os.getcwd()
CURR_PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-1])
print(ROOT_PATH)
print(CURR_PATH)
config_path = CURR_PATH+"/ai_files/config"
model_path = CURR_PATH+"/ai_files/nlp_smithing.weights.h5"
vc_path = CURR_PATH+"/ai_files/vectornize"
config=None
model=None
vc = None
y_label = ["정상문자","스미싱문자","알수없음"]
if config_path and model_path and vc_path:
    with open(config_path,"rb") as fp:
        config = pickle.load(fp)
vc = tf.keras.layers.TextVectorization(
    max_tokens=config["vocab_size"]-1,
    standardize='lower_and_strip_punctuation',
    split='whitespace',
    output_mode='int',
    output_sequence_length=config["cut_length"],
    pad_to_max_tokens=True,
    encoding='utf-8',
    vocabulary=config["vocab"]
)
print(tf.__version__)
# 모델구성
from tensorflow.keras import Input,Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
model = Sequential()
model.add(Input((config["cut_length"],)))
emb_1 = Embedding(
    config["vocab_size"]+1,
    8,
    mask_zero=True)
model.add(emb_1)
lstm_1 = LSTM(
    16,
    activation='tanh',
    recurrent_activation='sigmoid',
    dropout=0.3,
    recurrent_dropout=0.3,
    return_sequences=True
)
lstm_2 = LSTM(
    8,
    activation='tanh',
    recurrent_activation='sigmoid',
    dropout=0.3,
    recurrent_dropout=0.3,
    return_sequences=False
)
model.add(lstm_1)
model.add(lstm_2)
model.add(Dense(128,activation="relu",kernel_regularizer=tf.keras.regularizers.L2(0.0005)))#L2 규제
model.add(Dropout(0.5))
model.add(Dense(16,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(3,activation="softmax"))
adam = tf.keras.optimizers.Adam(
    learning_rate=0.0005,
    beta_1=0.85,
    beta_2=0.995)
#res = model(x_train)
#print(res.shape)
model.compile(loss="categorical_crossentropy",optimizer=adam,metrics=["acc"])
model.load_weights(model_path)
import pandas as pd
from konlpy.tag import Okt
#model, config, vc(textVectornize)
def preprocessing(message):
    #1. 정규표현으로 특수문자 제거
    message = pd.Series(message)
    reg_data = r"[^\sㄱ-ㅎ가-힣a-zA-Z0-9]"  # 한글 숫자 공백 이외를 지정
    message = message.replace(to_replace=reg_data, regex=True, value="")  # pandas의 serise 함수
    message = message.replace(r"\n", value=" ", regex=True)
    message = message.to_numpy()
    #2. 불용어와 형태소 분류
    stopword = ["은", "는", "이", "가", "에서", "하다", "들", "좀", "걍", "도", "요", "랑",
                "흠", "에게", "나다", "데", "있다", "의", "을", "를", "그", "로", "습니다"]
    # 단어별로 형태소 분류후 불용단어를 제거하면 됩니다. - okt 코랩 설치용
    # !curl -s https://raw.githubusercontent.com/teddylee777/machine-learning/master/99-Misc/01-Colab/mecab-colab.sh | bash
    okt = Okt()
    messages = []
    token_word = okt.morphs(message[0], stem=True)
    print(token_word)
    messages.append(" ".join([w for w in token_word if not w in stopword]))
    #3. 정수로 변경
    messages = vc(messages)
    res =run_predict(messages)
    return res[0].tolist(),y_label[np.argmax(res[0])]
def run_predict(x_pred):
    #정수로 변경된 데이터를 수신항 예측분석
    return model.predict(x_pred)
if __name__=="__main__":
    res = preprocessing("안녕하세요 내 이름은 홍길동이에요")
    print(res)
