var articlesApproved = document.getElementById("Approved");
var articlesOnChecked = document.getElementById("OnCheck");
var paginatorApproved = document.getElementById("pag_Approved");
var paginatorOnChecked = document.getElementById("pag_OnCheck");

function TabOnChecked(){
    if (document.getElementById("radio-1").checked){
        articlesApproved.style.display = "block";
        articlesOnChecked.style.display = "none";
        paginatorApproved.style.display = "block";
        paginatorOnChecked.style.display = "none";
    }
    else{
        articlesApproved.style.display = "none";
        articlesOnChecked.style.display = "block";
        paginatorApproved.style.display = "none";
        paginatorOnChecked.style.display = "block";
    }
}
