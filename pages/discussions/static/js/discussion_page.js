function new_comment(node_id) {
    // Get the modal
    var modal = document.getElementById('simpleModal' + node_id);

    //function openModal(){
    modal.style.display = 'block';
    return node_id;
}


function closeModal(node_id) {
    var modal = document.getElementById('simpleModal' + node_id);

    modal.style.display = 'none';
}

function rank_comment(node_id) {
    // Get the modal
    var modal = document.getElementById('rank_Modal' + node_id);

    //function openModal(){
    modal.style.display = 'block';
    return node_id;
}

function merge_comment(node_id) {


    document.querySelectorAll('[class*=merge_checkbox]')
        .forEach( x=> x.setAttribute("display","none"))
    return node_id;
}


function close_rank_Modal(node_id) {
    var modal = document.getElementById('rank_Modal' + node_id);

    modal.style.display = 'none';
}

function close_merge_Modal(node_id) {
    var modal = document.getElementById('merge_Modal' + node_id);
    modal.style.display = 'none';
}

function change_star(x) {
    var star = document.getElementById('disc' + x);
    star.setAttribute('class', 'fa fa-star')
}

function change_edit() {
    yy = document.getElementById('boaz');
    yy.setAttribute('background-color', 'green');
    alert('sdff');

}
