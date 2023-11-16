//아이콘을 클릭했을 때 호스트 서버로 html 넘겨주기 
chrome.action.onClicked.addListener(async (tab) => {
  chrome.scripting.executeScript({ // 웹페이지에서 스크립트 실행
    target: { tabId: tab.id }, // tabId는 현재 클릭된 탭의 식별자
    function: () => {
      
      let data = JSON.stringify({
        source : document.documentElement.innerHTML
      });
      const request = new XMLHttpRequest(); // 요청과 응답을 받아올 XHR 객체 생성
     
      //해당 웹페이지의 html을 호스트 서버로 보내기 -> ec2서버로 보내기
      request.open('POST', 'http://54.180.153.178:5000/naverblog', true);
      request.setRequestHeader('Content-Type', 'application/json');
      request.send(data);

      //아이콘 클릭 후 크롤링 끝나면 alert 와 css 바꿔주기
      request.addEventListener('load', function(){
        if (this.readyState === 4 && this.status === 200){
          var responseData = JSON.parse(request.responseText);//예측값 리스트 반환
          for (var i=0; i < responseData.length; i++){
            if(responseData[i] === 1){
              var target = document.getElementsByClassName('view_wrap')[i]
              target.style.border = '3px solid red';
            }
            else {
              var target2 = document.getElementsByClassName('view_wrap')[i]
              target2.style.border = '3px solid blue';
            }
          }
          alert("Done!"); }
        })

      // 스크롤 이벤트에 대한 처리
      let PostCount = 30;
      let isScrolling = false;
      let scrolledCount = 0; // 추가: 서버로 전송한 스크롤 이벤트 횟수


      document.addEventListener('scroll', function(){
        isScrolling = true;
      });

      setInterval(function(){
        if(isScrolling){
          let currentPostCount = document.querySelectorAll('.view_wrap').length;

          // 클래스 개수가 30개씩 늘어날 때마다 서버에 상태 전송
          if (currentPostCount - PostCount >= 1){
              sendDataToserver(scrolledCount);
              scrolledCount += 1;
              //alert ("scroll!")
          }
          PostCount = currentPostCount;
        }
        isScrolling = false;
      }, 500); //0.5초단위로 스크롤 상태 확인

      function sendDataToserver(){
        let data = JSON.stringify({
          source : document.documentElement.innerHTML,
          scrollCount: scrolledCount 
      });
      
      const request = new XMLHttpRequest();
      request.open('POST', 'http://54.180.153.178:5000/naverblog/scroll', true);
      request.setRequestHeader('Content-Type', 'application/json');
      request.send(data);
      request.addEventListener('load', function(){
        if (this.readyState === 4 && this.status === 200){
          var responseData = JSON.parse(request.responseText);//예측값 리스트 반환
          for (var i=0; i < responseData.length; i++){
            if(responseData[i] === 1){
              var target = document.getElementsByClassName('view_wrap')[i + (scrolledCount * 30)]
              target.style.border = '3px solid red';
            }
            else {
              var target = document.getElementsByClassName('view_wrap')[i + (scrolledCount * 30)]
              target.style.border = '3px solid blue';
            }
          }
          alert("Done!"); }
      })
      }
    }
  });
});



