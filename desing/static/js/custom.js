var listNameFornewArticle = ["article_title", "article_small_text", "article_small_text", "myfield"]

for (let i =0; i < listNameFornewArticle.length; i++){
    document.getElementById('form').querySelector(`[name="${listNameFornewArticle[i]}"]`).classList.add("form-control");
    document.getElementById('form').querySelector(`[name="${listNameFornewArticle[i]}"]`).classList.add("form-control-custom");
}

// console.log(document.getElementByClass('markdownx-preview'))
document.getElementsByClassName('markdownx-preview')[0].setAttribute("id", "content_det");
// document.getElementByClass('markdownx-preview').classList.add("form-control-custom");


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