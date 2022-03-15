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
var listNameFornewArticle = ["article_title", "article_small_text", "article_small_text", "myfield",
                             "avatar", "username", "email", "description", "where_you_leave", "date_of_birth",
                             "password", "password2", "old_password", "new_password1", "new_password2", "markdownx-preview"]


for (let i =0; i < listNameFornewArticle.length; i++){
    if (document.getElementById('form') == null || document.getElementById('form').querySelector(`[name="${listNameFornewArticle[i]}"]`) == null) continue;
    document.getElementById('form').querySelector(`[name="${listNameFornewArticle[i]}"]`).classList.add("form-control");
    document.getElementById('form').querySelector(`[name="${listNameFornewArticle[i]}"]`).classList.add("form-control-custom");
}

if (document.getElementsByClassName('markdownx-preview')[0]){
    document.getElementsByClassName('markdownx-preview')[0].setAttribute("id", "content_det");
}

if (document.getElementById('login_block')){
    document.getElementById('login_block').querySelector(`[name="username"]`).classList.add("form-control");
    document.getElementById('login_block').querySelector(`[name="username"]`).classList.add("form-control-custom");
    document.getElementById('login_block').querySelector(`[name="password"]`).classList.add("form-control");
    document.getElementById('login_block').querySelector(`[name="password"]`).classList.add("form-control-custom");
}

var button = document.getElementsByClassName("login");
var img_logo = document.getElementById("mainLogo");

// KaTex
function KaTex() {
'use strict';

var katexMath = (function () {
    var maths = document.querySelectorAll('.arithmatex'),
        tex;

    for (var i = 0; i < maths.length; i++) {
      tex = maths[i].textContent || maths[i].innerText;
      if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
        katex.render(tex.slice(2, -2), maths[i], {'displayMode': false});
      } else if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
        katex.render(tex.slice(2, -2), maths[i], {'displayMode': true});
      }
      if (tex.startsWith('$') && tex.endsWith('$')) {
        katex.render(tex.slice(1, -1), maths[i], {'displayMode': false});
      } else if (tex.startsWith('$$') && tex.endsWith('$$')) {
        katex.render(tex.slice(2, -2), maths[i], {'displayMode': true});
      }
    }
});

(function () {
  var onReady = function onReady(fn) {
    if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      document.attachEvent("onreadystatechange", function () {
        if (document.readyState === "interactive") {
          fn();
        }
      });
    }
  };

  onReady(function () {
    if (typeof katex !== "undefined") {
      katexMath();
    }
  });
})();

};

KaTex();
//

function handleButtonClick() {
    halfmoon.toggleDarkMode()
    if(!$("body").hasClass("dark-mode")) {
        img_logo.src = "../../static/img/logo_dm.svg"
    }
    else{
        img_logo.src = "../../static/img/logo_lm.svg"
    }
}