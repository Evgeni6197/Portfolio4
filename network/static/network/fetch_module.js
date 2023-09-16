export function fetch_comments(post_id){

    fetch('/get_comments/'+`${post_id}`)
    .then(response => response.json())
    .then(result => {

        if (result.success){

            document.getElementById('initial_post_place').innerHTML =  result.post_content;
            document.getElementById('previous_comments_place').innerHTML = '';

            if (result.comments.length){
                for(let item_data of result.comments) {                    
                    const prev_comment_div=document.createElement('div');
                    document.getElementById('previous_comments_place').append(prev_comment_div);
                    prev_comment_div.setAttribute('class', 'specific_comment_container overflow wrap');
                    prev_comment_div.innerHTML = item_data;
                }
            } else {
                document.getElementById('previous_comments_place').innerHTML = "No comments yet";
            }
            
        } else {
            console.log ('error in data retrieving');
        }    
    });
}