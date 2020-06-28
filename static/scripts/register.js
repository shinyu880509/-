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
    