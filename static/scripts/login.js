function login() {
var username = document.getElementById("username");
var pass = document.getElementById("password");
if (username.value == "") {
        alert("請輸入帳號");
    } else if (pass.value  == "") {
        alert("請輸入密碼");
    } else if(username.value == "1" && pass.value == "1"){
        window.location.href="/index";
    } else {
        alert("請輸入正確的帳號和密碼！")
    }
}