function register() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
    var confirm = document.getElementById("confirm");
    var userEmail = document.getElementById("email");
    var c = userEmail.value.indexOf("@");
    var cc = userEmail.value.indexOf(".");
    if (username.value == "") {
            alert("請輸入帳號");
        } 
        else if (pass.value  == "") {
            alert("請輸入密碼");
        } 
        else if (confirm.value  == "") {
            alert("請確認密碼");
        }
        else if (confirm.value  != pass.value) {
            alert("密碼與確認密碼不同");
        }
        else if (c == -1 || cc == -1){
            alert("請輸入正確的信箱");
        }
        else{
            window.location.href="/registeCheck/" + username.value + "/" + pass.value + "/" + userEmail.value; /*------------跳回login-------------*/ 
    }
    /*--------------註冊資料放進資料庫-------------*/  

                    /*柏恩不會寫*/

    /*-------------------------------------------*/ 
}

/*-------寄信-------*/
function ee() {
    var username = document.getElementById("username");
    var emailname = document.getElementById("email");
    var c = emailname.value.indexOf("@");
    var cc = emailname.value.indexOf(".");
    if (username.value == ""){
        alert("請輸入帳號");
    }
    else if (emailname.value == "") {
        alert("請輸入信箱");
    }
    else if (c == -1 || cc == -1){
        alert("請輸入正確的信箱");
    }
    else{
        window.location.href="/message/" + emailname.value + "/" + username.value; 
    }
}

/*-------驗證-------*/
function revA() {
    var pw = document.getElementById("pw");
    var npw = document.getElementById("npw");
    var va = document.getElementById("va");
    if (pw.value == ""){
        alert("請輸入密碼");
    }
    else if (npw.value == "") {
        alert("請確認密碼");
    }
    else if (va.value == "") {
        alert("請輸入驗證碼");
    }
    else{
        window.location.href="/revise/" + va.value + "/" + pw.value; 
    }
}
    