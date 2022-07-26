function openDeleteModal(articleId){
    var modal = document.getElementById("container");
    var linkToDelete = document.getElementById("modal_delete_art");
    if (modal.style.visibility == "hidden"){
        modal.style.visibility = "visible";
        modal.style.opacity = 1;
        linkToDelete.href += articleId;
    }
    else{
        modal.style.visibility = "hidden";
        modal.style.opacity = 0;
        linkToDelete.href = linkToDelete.href.slice(0, 16);
    }
}