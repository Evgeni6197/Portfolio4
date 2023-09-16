import {fetch_comments} from './fetch_module.js';

document.querySelectorAll('.comment').forEach((comment_link)=>{

    comment_link.addEventListener('click',(event)=>{

        const post_id = event.target.dataset.id;
        const initial_heading = document.getElementById("heading_place").innerHTML;
        const return_to_post_button = document.getElementById("return_to_post_button");

        document.getElementById("pagination_prev_but_place").classList.add('invisible');
        document.getElementById("pagination_next_but_place").classList.add('invisible');
        document.getElementById("new_post_button_place").classList.add('invisible');
        document.getElementById("general_container").classList.add('invisible');

        document.getElementById("return_to_posts_button_place").classList.remove('invisible');
        document.getElementById('comments_place').classList.remove('invisible');        
        document.getElementById("heading_place").innerHTML = "<h3>Comments</h3>";
        document.getElementById('comments_place').setAttribute('data-post_id',post_id);

        return_to_post_button.setAttribute('data-initial_heading',initial_heading);
        return_to_post_button.addEventListener('click', inverse_visibility);

        fetch_comments(post_id);    
    });
});

function inverse_visibility(event){

    const initial_heading = event.target.dataset.initial_heading;
    document.getElementById("pagination_prev_but_place").classList.remove('invisible');
    document.getElementById("pagination_next_but_place").classList.remove('invisible');
    document.getElementById("new_post_button_place").classList.remove('invisible');
    document.getElementById("general_container").classList.remove('invisible');

    document.getElementById("return_to_posts_button_place").classList.add('invisible');
    document.getElementById('comments_place').classList.add('invisible'); 
    document.getElementById("heading_place").innerHTML = initial_heading; 
    
    document.getElementById('previous_comments_place').innerHTML=' '
    document.getElementById('initial_post_place').innerHTML= ' '
}

