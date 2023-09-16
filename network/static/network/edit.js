document.querySelectorAll('.edit').forEach((edit_link)=>{

    edit_link.addEventListener('click',(event)=>{

        const post_id=event.target.dataset.post_id;

        const textarea = document.getElementById(`${post_id}`);
        textarea.parentElement.classList.remove('invisible');
        const content_container = textarea.parentElement.nextElementSibling.lastElementChild;
        const former_content = content_container.innerHTML;
        const cancel_button = textarea.nextElementSibling.nextElementSibling;
        
        textarea.value = former_content;
        const submit_button = textarea.nextElementSibling;
        const posts = document.getElementsByClassName('post');

        for (post of posts){
            post.classList.add('blur');
        }  

        cancel_button.addEventListener('click',()=>{

            textarea.parentElement.classList.add('invisible');
            for (post of posts){
                post.classList.remove('blur');
            }
        })
        

        submit_button.addEventListener('click',()=>{

            for (post of posts){
                post.classList.remove('blur');
            }

            content_container.innerHTML = textarea.value;

            fetch('/edit_post/0',{
                'method'  : 'PUT',
                'body': JSON.stringify({
                    post_id: post_id,
                    new_content: textarea.value,
              })
            }); 
            
            setTimeout(()=>{fetch_datetime_editing(post_id)}, 500);

            textarea.parentElement.classList.add('invisible');
        });       
    });
});

function fetch_datetime_editing(post_id){

    fetch('/edit_post/'+`${post_id}`)
    .then(response => response.json())
    .then(result => {
        
        document.getElementsByClassName(
            result.post_id).item(0).innerHTML = "Edited at " + result.datetime_editing + '&nbsp&nbsp&nbsp&nbsp';
    });
}


