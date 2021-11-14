var button = document.getElementsByClassName("login");
var img_logo = document.getElementById("mainLogo");

function handleButtonClick() {
    halfmoon.toggleDarkMode()
    if(!$("body").hasClass("dark-mode")) {
        img_logo.src = "../images/logo_dm.svg"
    }
    else{
        img_logo.src = "../images/logo_lm.svg"
    }
}