function login() {
var username = document.getElementById("username");
var pass = document.getElementById("password");
if (username.value == "") {
        alert("請輸入帳號");
    } else if (pass.value  == "") {
        alert("請輸入密碼");
    } else {
        window.location.href="/userLogin/" + username.value + "/" + pass.value;
    }
}