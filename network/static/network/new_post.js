const new_post_button = document.getElementById('new_post_button');

new_post_button.addEventListener('click',open_new_post_textarea);

function open_new_post_textarea(){
    
    const new_post = document.getElementsByClassName('new_post').item(0);
    const cancel_button = document.getElementById('cancel_new_post');

    new_post_button.removeEventListener('click',open_new_post_textarea);
    new_post_button.classList.remove('top_button');
    new_post.classList.remove('invisible');

    const posts = document.getElementsByClassName('post');

    for (post of posts){
        post.classList.add('blur');
    }  

    cancel_button.addEventListener('click',()=>{
 
        new_post.classList.add('invisible');

        new_post_button.setAttribute('class','top_button');
        new_post_button.addEventListener('click',open_new_post_textarea);

        for (post of posts){
            post.classList.remove('blur');
        }  
    });                        
};