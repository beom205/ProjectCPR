//버튼을 클릭하면 모달창이 뜨도록
var btn = document.getElementById("btn");
var modal = document.querySelector(".modal");
function modalHendler(){
    modal.style.display="block";
}
btn.addEventListener("click",modalHendler);