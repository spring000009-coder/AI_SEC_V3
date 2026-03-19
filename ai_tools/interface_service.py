#웹 모듈과 Ai 모듈 연동
from ai_tools.crypto_coin.coin_model import (time_step,get_datas,preprocessing_datas,
                                             create_datas,convt_data,predict_datas)
from ai_tools.smithing_anal.sms_model import preprocessing
def get_service_data(service_datas):
    if service_datas["information"] == "coin":
        res_datas = get_datas(service_datas["coin_name"]) # 데이터 다운로드및 추출
        gen_datas = preprocessing_datas(res_datas) # 로부스트 전처리 스케일링
        rnn_xdatas = create_datas(gen_datas)#타임스텝길이만큼의 시계열 데이터 생성부
        print("최종모양:",rnn_xdatas.shape)
        # res = convt_data(rnn_xdatas[:,-1,:]) # 마지막 데이터 확인 작업
        # for i in res[0]:
        #     print(i)
        current_pred\
            = predict_datas(rnn_xdatas,int(service_datas["coin_day"]))#(데이터,일수)
        pred_dict = convt_data(current_pred)
        # print(rnn_xdatas.shape)
        # print("current_pred:",current_pred.shape)
        # print("rnn_xdatas:",rnn_xdatas.shape)
        # #최종모양: (1, 90, 6)  90개중 마지막 데이터만 추출 하여 이전데이터로 변경작업
        # print("==== 마지막 데이터 수집 확인")#(1,90,1))
        # print(rnn_xdatas.reshape(time_step,-1).shape)
        pred_dict["previous"]\
            =convt_data(rnn_xdatas.reshape(time_step,-1))["pred_info"]
        # print(pred_dict["previous"][0]) #복원된 가격 확인
        return pred_dict
        # print(pred_res)#(1, 6) 내일 예측가격
        # for i in pred_res[0]:
        #     print(i)
    elif service_datas["information"] == "sms":
        return preprocessing(service_datas["sms_message"])