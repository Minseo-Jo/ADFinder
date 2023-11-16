/*
var script = document.createElement('script');
script.src =  chrome.runtime.getURL('jquery-3.7.1.min.js');
document.head.appendChild(script);


script.onload = function(){
current_url = window.location.href;
alert("nice!")
$.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000/naverblog', //데이터를 전송하고자하는 서버 주소
    crossDomain: true,

    data : { url: current_url },
    dataType: 'json', // json 형태로 주소를 넘겨준다.

    //요청이 성공해서 정상적인 응답을 받으면 실행되는 콜백함수
    //responseData : 서버로부터 받은 데이터
    success: function(responseData, textStatus, jqXHR) { 
        alert("nice!");
        var value = responseData.someKey; // someKey == 1 

        if (value == "1") {
            var target = document.getElementsByClassName("bx")[0];
            target.style.border = '2px solid red';
        }
    },
    error: function (responseData, textStatus, errorThrown) {
        alert('POST failed.');
    }
  });

};
*/

/*
let data = JSON.stringify({
    url : window.location.href
});

const request = new XMLHttpRequest();

request.addEventListener('load', function () {
    if (this.readyState === 4 && this.status === 200) {
        var responseData = JSON.parse(this.responseText); // JSON 데이터 파싱
        if (responseData.someKey === "1") {
            var target = document.getElementById('sp_blog_1');
            target.style.border = '2px solid red';
        }
    }
});

request.open('POST', 'http://localhost:5000/naverblog', true);
request.setRequestHeader('Content-Type', 'application/json');
request.send(data);

*/

//스크립트에서 html의 class길이가 30개늘어났을때
// 요청하는 데이터는 json 의 스크롤 감지


/*
let PostCount = 30;
let isScrolling = false;

document.addEventListener('scroll', function(){
    isScrolling = true;
});

setInterval(function(){
    if(isScrolling){
        let currentPostCount = document.querySelectorAll('.view_wrap').length;

        // 클래스 개수가 30개씩 늘어날 때마다 서버에 상태 전송
        if (currentPostCount - PostCount >= 1){
            sendDataToserver();
            alert ("scroll!")
        }
        PostCount = currentPostCount;
    }
    isScrolling = false;
}, 1000); //1초단위로 스크롤 상태 확인

function sendDataToserver(){
    let data = JSON.stringify({
        source : window.location.href
    });

    const request = new XMLHttpRequest();
    request.open('POST', 'http://localhost:5000/naverblog/scroll', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(data);

}
*/


