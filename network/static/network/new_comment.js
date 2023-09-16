
import {fetch_comments} from './fetch_module.js';

document.getElementById("new_comment_button").addEventListener('click',()=>{

    const new_comment_content = document.getElementById("comment_textarea").value;
    const post_id = document.getElementById('comments_place').dataset.post_id;

    if (new_comment_content.trim()){

        console.log('put fetch')
        fetch('/new_comment',{
            "method":"PUT",
            "body":JSON.stringify({
                post_id:post_id,
                new_comment_content:new_comment_content
            })
        })
    }
  
    
    document.getElementById("comment_textarea").value =''

    setTimeout(()=>{fetch_comments(post_id)}, 500);
})