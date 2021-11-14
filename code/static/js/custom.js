function Adblock(){
    var modal = document.getElementById("modal_full");
    var modal_close1 = document.getElementById("ok");
    var modal_close2 = document.getElementById("pidr");
    var flag_reaction = 0;
    if (!noAdBlock) {
        modal.style.display = "block";
    }
    modal_close1.onclick = function() {
        modal.style.display = "none";
        flag_reaction = 1;
    }
    modal_close2.onclick = function() {
        modal.style.display = "none";
        flag_reaction = 2;
    }
    if(flag_reaction == 1){alert("Спасибо за понимание ＼(＾▽＾)／");}
    if(flag_reaction == 2){alert("Ну ладно ಠ_ಠ");}
}

Adblock();


var button = document.getElementsByClassName("login");
var img_logo = document.getElementById("mainLogo");

function handleButtonClick() {
    halfmoon.toggleDarkMode()
    if(!$("body").hasClass("dark-mode")) {
        img_logo.src = "../../static/img/logo_dm.svg"
    }
    else{
        img_logo.src = "../../static/img/logo_lm.svg"
    }
}