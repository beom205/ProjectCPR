//이미지에 이벤트 핸들러 넣기-> 1. img src가져오기 2. class active 넣어서 css바꾸기 3.다른 class는 active 지우기  
function setPhotoListEvent(){
  var lists = document.querySelectorAll(".list li");
  var classified_img = document.getElementById("classified_img");
  var cam_img = document.getElementById("cam_img");
  var currentimg;

  for (var i=0 ; i<lists.length ;i++){
    lists[i].addEventListener('click',clickHandler);
  }
  
  //초기 첫번째 이미지 클릭
  lists[0].click();

  function clickHandler(e) {
    console.log("클릭")
    if(currentimg){
        currentimg.classList.remove('active');
    }
    this.classList.add('active');
    currentimg=this;
    var classified_img_src=this.querySelector('img').getAttribute('src');
    var cam_img_data = this.querySelector('input').value;
    // var img_src=img.getAttribute('src');
    classified_img.setAttribute("src",classified_img_src);
    cam_img.setAttribute("src",cam_img_data);
    
    click_img = document.querySelector("#big p");
    click_img.style.display="none";

    // getCamImage2(img_src);
  }

  function getCamImage(img_path){
    console.log("clicked getCamImage")
    // classified_img.setAttribute("src",img_path); 
    var data = { img_path : img_path};
    $.ajax({
      type : 'POST',
      contentType:'application/json',
      url:'/cam',
      data: JSON.stringify(data),
      success: function(result){
        // console.log("result : ",result);
        console.log("성공")
        var cam_img = document.getElementById("cam_img");
        cam_img.dataset.path = "dd";
        // cam_img.setAttribute("src",img_path);
        // classified_img.setAttribute("src",img_path);
        classified_img.setAttribute("src",result);
      }
    });
  }
  function getCamImage2(img_path){
    console.log("clicked getCamImage")
    // classified_img.setAttribute("src",img_path); 
    var data = { img_path : img_path};
    $.ajax({
      url: "/cam2", // fix this to your liking
      type:"POST",
      data: JSON.stringify(data),
      cache: false,
      processData:false,
      contentType:'application/json',
      error: function(result){
        console.log("upload error" , result);
        console.log(result.getAllResponseHeaders());
      },
      success: function(result){
        console.log("성공")
        // alert("hello"); // if it's failing on actual server check your server FIREWALL + SET UP CORS
        bytestring = result['status'];
        image = bytestring.split('\'')[1];
        classified_img.setAttribute('src' , 'data:image/jpeg;base64,'+image);
      }
    });
  }
}
