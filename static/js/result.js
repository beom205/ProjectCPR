//이미지에 이벤트 핸들러 넣기-> 1. img src가져오기 2. class active 넣어서 css바꾸기 3.다른 class는 active 지우기
var lists = document.querySelectorAll(".list li");
var big_image = document.querySelector("#big img");
var currentimg;

for (var i=0 ; lists.length ;i++){
lists[i].addEventListener('click',clickHandler);
}

function clickHandler(e) {
if(currentimg){
    currentimg.classList.remove('active');
}
this.classList.add('active');
currentimg=this;
var img=this.querySelector('img');
var img_src=img.getAttribute('src');
big_image.setAttribute("src",img_src);
click_img = document.querySelector("#big p");
click_img.style.display="none";
}