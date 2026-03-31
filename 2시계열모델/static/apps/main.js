console.log("== js action ==")
//jquery({})
var current_id="coin"
$(()=>{
    console.log("2. 모든 document 라 메모리에 로드된 후에 작동됩니다.")
    $(`#${current_id}`).css("display","block")
        .attr("src",`/static/images/${current_id}_img.png`)
    $("li").on("mouseover",function(){
        let img_id = $(this).attr("info")
        if(current_id != img_id){
            current_id = img_id
            let img_path = `/static/images/${$(this).attr("info")}_img.png`
            $(".sec_img").css("display","none")
            $(`#${img_id}`).css("display","block").attr("src",img_path)
        }
    })
    $("li").on("click",function(){
        $("#result_data").html("")
        const info = $(this).attr("info")
        const container = $("#user_data")
        if(info=="coin"){
            $("#analbtn").text("코인분석하기")
            container.html(coin_ui)
        }else if(info=="sms"){
            $("#analbtn").text("문자분석하기")
            container.html(sms_ui)
            $("#sms_msg").val("")
        }
        else if(info=="gen"){
            container.html(gen_ui)
            //???????????????????????
            $("#analbtn").text("이미지생성하기")
        }
        $("#anal_content h3").text($(this).attr("describ"));
        $(".coverui").css("display","block")
        //서버로 보낼 메뉴의 종류 타입 설정
        $("#anal_content h3").attr("information",info)
    })
    $("#x_btn,#anal_win").on("click",function(){
        $(".coverui").css("display","none")
    })
    $("#analbtn").on("click",async ()=>{
        // 필요 데이터 수집후 서버로 전송
        const information = $("#anal_content h3").attr("information")
        let datas = {}
        if(information=="coin"){
            const coin_name = $("#coin_name").val()
            const coin_model = $("#cmodel").val()
            const coin_day = $("#cday").val()
            datas={information,coin_name,coin_model,coin_day}
        }else if(information=="sms"){
            if(!$("#sms_msg").val()){
                alert("문구를 입력하세요")
                return
            }
            datas = {information:"sms",sms_message:$("#sms_msg").val()}
        }else if(information=="gen"){
            datas = {information:"gen",loc_val:$("#loc_val").val(),scale_val:$("#scale_val").val()}
        }
        const res = await fetch("/analize",
            {method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify(
                    datas
                )
            }
         )
        const resp = await res.json()
        console.log(resp)
        if(information=="coin"){
           create_coinui(resp)
        }else if(information=="sms"){
            create_smsui(resp,$("#sms_msg").val())
            $("#sms_msg").val("")
        }else if(information=="gen"){
            create_genui(resp)
        }
    })
})
function create_genui(img_path){
    const jq_res = $("#result_data")
    let inHtml =`<h4>분석결과 표기</h4>`
    if($("#result_data img").size()){
        $("#result_data").append(
            `<img src="/static/${img_path}" style="width:96px;height:96px}"/>`
        )
    }else{
        inHtml+=`<img src="/static/${img_path}" style="width:96px;height:96px}"/>`
        jq_res.html(inHtml)
    }
}
function create_smsui(ui_datas,message){
    const jq_res = $("#result_data")
    let inHtml = `<h4>분석결과 표기</h4>`
    const maxval = Math.max(ui_datas[0][0],ui_datas[0][1],ui_datas[0][2])
    const oval = `
    <div>
        <span style="margin-right:1rem;display:inline-block;width:68%;height:3rem">
            ${message}
        </span>
        <span>${(maxval*100).toFixed(2)}% 확률로 ${ui_datas[1]}</span>
        <span class="oval" style="background:darkgreen">
            ${(ui_datas[0][0]*100).toFixed(2)}%
        </span>
        <span class="oval" style="background:darkred">
            ${(ui_datas[0][1]*100).toFixed(2)}%
        </span>
        <span class="oval" style="background:gold">
            ${(ui_datas[0][2]*100).toFixed(2)}%
        </span>
    </div>
      `
    jq_res.append(oval)
}
function create_coinui(ui_datas){
    const jq_res = $("#result_data")
    let inHtml = `<h4>분석결과 표기</h4>`
    console.log(ui_datas)
    // 인덱스 상수 선언
    const opening_price=0
    const high_price=1
    const low_price=2
    const trade_price=3
    const prev_closing_price=4
    const change_rate=5
    inHtml +=
    `
    <div class="box">
        <p>오늘 가격정보</p>
        <p><span class="unit_title">최 고 가 </span>
            <span class="unit_val">${ui_datas["previous"].at(-1)[high_price].toLocaleString()}</span></p>

        <p><span class="unit_title">종가/현재가 </span>
            <span class="unit_val">${ui_datas["previous"].at(-1)[trade_price].toLocaleString()}</span></p>

        <p><span class="unit_title">최 저 가 </span>
            <span class="unit_val">${ui_datas["previous"].at(-1)[low_price].toLocaleString()}</span></p>

        <p><span class="unit_title">등 락 율 </span><span>
        ${parseInt(ui_datas["previous"].at(-1)[change_rate]
            *100*100)/100}%</span></p>
    </div>
    `
    let preDate = new Date()
    const cnt = ui_datas["previous"].length-1
    preDate.setDate(preDate.getDate()-cnt)
    let series_datas=[];
     //[시가, 고가, 저가, 종가]
    for(const pv of ui_datas["previous"]){
    console.log(preDate.toLocaleDateString())
        series_datas.push({x:preDate.toLocaleString("ko-KR",{
            year:"numeric",month:"2-digit",day:"2-digit"
        }),y:[pv[opening_price],pv[high_price]
        ,pv[low_price],pv[trade_price]]})
        preDate.setDate(preDate.getDate()+1)

    }
    let curDate = new Date()
    for(const pred_val of ui_datas["pred_info"]){
       curDate.setDate(curDate.getDate()+1)
       series_datas.push({x:curDate.toLocaleDateString("ko-KR",{
            year:"numeric",month:"2-digit",day:"2-digit"
        }),y:[pred_val[opening_price],pred_val[high_price]
        ,pred_val[low_price],pred_val[trade_price]]})
       const updown = (pred_val[trade_price]/pred_val[opening_price]-1)
       const gap_updn = Math.abs(pred_val[change_rate]-updown)
       inHtml +=
        `
        <div class="box">
            <p style="color:${updown>0?'red':'blue'}">${curDate.toLocaleDateString()}</p>
            <p><span class="unit_title">최 고 가 </span>
                <span class="unit_val">${pred_val[high_price].toLocaleString()}</span></p>

            <p><span class="unit_title">종가/현재가 </span>
                <span class="unit_val">${pred_val[trade_price].toLocaleString()}</span></p>

            <p><span class="unit_title">최 저 가 </span>
                <span class="unit_val">${pred_val[low_price].toLocaleString()}</span></p>

            <p><span class="unit_title">등 락 율 </span><span>
            ${parseInt(updown*100*100)/100}%</span></p>
            <p><span class="unit_title">오 차 율</span><span>${parseInt(gap_updn*100*100)/100}%</span>
        </div>
        `
    }
    console.log("length")
    console.log(series_datas.length)
    inHtml+=`<div id="chart"></div>`
    jq_res.html(inHtml)
    let options = {
      chart: {
        type: 'candlestick',
        height: 350
      },
      series: [{
        data: series_datas
      }]
    };
    console.log(series_datas)
    const chart = new ApexCharts($("#chart")[0],options)
    chart.render();
}
//<div>

//<!--                //현재가격정보 DarkRed  배경 - 가격상승, DarkGreen - 가격 하락정보-->
//<!--                // 예측 가격 정보 LightCoral  배경- 가격상승예측, LightGreen 배경 하락정보-->
//    <div class="box" style="background:DarkRed;color:white">
//        <p>2/28일 예측정보</p>
//        <p><span>최고가</span><span>350</span></p>
//        <p><span>종 &nbsp;가</span><span>340</span></p>
//        <p><span>최저가</span><span></span>320</p>
//        <p><span>등락율</span><span></span>+10%</p>
//    </div>
//    <div class="box">
//        <p>3/1일 예측정보</p>
//        <p><span>최고가</span><span></span></p>
//        <p><span>종 &nbsp;가</span><span></span></p>
//        <p><span>최저가</span><span></span></p>
//        <p><span>등락율</span><span></span></p>
//    </div>
//</div>
const coin_ui = `
<div>
    <label>화 폐 명 <select id="coin_name">
        <option value="btc">BTC(비트코인)</option>
        <option value="eth">ETH(이더리움)</option>
        <option value="xrp">XRP(리플)</option>
    </select></label>
    <label>분석모델 <select id="cmodel">
        <option>L S T M</option>
        <option>CONVLSTM</option>
    </select></label><br>
    <label>분석일수 <input id="cday" type="number" value="5"></label>
</div>
`
const sms_ui = `
<div>
    <label>수신된 문자메시지를 입력하세요 <br>
        <textarea cols=100 rows=5 id="sms_msg"
         style="margin-bottom:1vh;padding:1rem">
        </textarea>
    </label>
</div>
`
const gen_ui = `
<div STYLE="padding:1rem">
    <form method="post" enctype="multipart/form-data">
        <input type="file" placeholder="이미지업로드 아지 미지원입니다">
        <label>loc value <input id="loc_val" type="number" value="0.0" max="3.0" min="-3.0 placehoder="loc 값을 입력하세요"/></label>
        <label>scale value <input id="scale_val" type="number" value="1.0" max="3.0" min="-3.0 placehoder="scale 값을 입력하세요"/></label>
    </form>
</div>
`