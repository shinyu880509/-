function register() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
    var confirm = document.getElementById("confirm");
    if (username.value == "") {
            alert("請輸入帳號");
        } else if (pass.value  == "") {
            alert("請輸入密碼");
        } else if (confirm.value  == "") {
            alert("請確認密碼");
        }else if (confirm.value  != pass.value) {
            alert("密碼與確認密碼不同");
        }else{
            alert("註冊成功");
            window.location.href="/login"; /*------------跳回login-------------*/ 
    }
    /*--------------註冊資料放進資料庫-------------*/  

                    /*柏恩不會寫*/

    /*-------------------------------------------*/ 
}

/*-------寄信-------*/
function ee() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
    var confirm = document.getElementById("confirm");
    var emailname = document.getElementById("email");
    var c = emailname.value.indexOf("@");
    if (username.value == ""){
        username = "a"
    }
    if (pass.value == ""){
        pass = "a"
    }
    if (confirm.value == ""){
        confirm = "a"
    }
    if (emailname.value == "") {
        alert("請輸入信箱");
    }
    else if (c!=-1){
        alert("信件已寄到 " + emailname.value + " 請確認");
        window.location.href="/message/" + emailname.value + "/" + username.value + "/" + pass.value + "/" + confirm.value; 
    }
    else{
        alert("請輸入正確的信箱");
    }
}
    