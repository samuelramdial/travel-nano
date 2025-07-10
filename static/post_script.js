// function postPagination(){
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let current_page = urlParams.get('page') || 1;
    

    // hide all posts by default
    let posts = document.querySelectorAll('.box-item');
    posts.forEach((post) => {
        post.style.display = 'none';
    });

    // show posts for current page
    let start_index = (current_page - 1) * 9;
    let end_index = start_index + 9;
    for (let i = start_index; i < end_index && i < posts.length; i++) {
        posts[i].style.display = 'block';
    }
// }
// document.querySelector('.nav-blog').addEventListener('click',()=>{
//   postPagination();
// })