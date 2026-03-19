from flask import Flask, render_template, request, jsonify
from ai_tools.interface_service import get_service_data
app = Flask(__name__)
# 라우팅
@app.route("/")
def main_rt():
    return render_template("main.html")
@app.route("/cryptocoin")
def cryptocoin():
    return "가상화폐 예측 페이지"
@app.route("/analize", methods=["POST"])
def analize():
    info_data = request.get_json()  # 클라이언트 데이터 수신부
    # print(info_data)#보낼 데이터 생성하는 로직
    result = get_service_data(info_data)
    return jsonify(result)  # 결과 데이터 클라이언트로 송신부

app.run(host="192.168.219.91", debug=True, port=1234)

"""
디렉토리 아키텍처
ai_tools >
  crypto_coin >
   - config
   - img

templates >
static >
   - images
   - css
   - apps
prefix : cryptocoin (cpc_)
"""