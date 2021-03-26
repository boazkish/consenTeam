function new_discussion_logged_in() {
    // Get the modal
    var modal = document.getElementById('simpleModal');

    //function openModal(){
    modal.style.display = 'block';
}
function new_discussion_not_logged_in() {
    // Get the modal
    var modal = document.getElementById('modal_not_logged_in');

    //function openModal(){
    modal.style.display = 'block';
}

function closeModal() {
    var modal = document.getElementById('simpleModal');

    modal.style.display = 'none';
}

function closeModal_not_logged_in() {
    var modal = document.getElementById('modal_not_logged_in');

    modal.style.display = 'none';
}

function change_star(x){
    var star = document.getElementById('disc'+x);
    star.setAttribute('class','fa fa-star')
}

