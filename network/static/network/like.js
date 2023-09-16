
document.querySelectorAll('.thumb_up').forEach((thumb_up)=>{

    thumb_up.addEventListener('click',(event)=>{

        const post_id = event.target.dataset.post_id;
        const like_status=event.target.dataset.like_status;
        let like_quantity = event.target.dataset.like_quantity;
        const sibling_thumb_down = event.target.parentElement.parentElement.lastElementChild.firstElementChild
        const sibling_dislike_status = sibling_thumb_down.dataset.dislike_status;

        fetch_like(post_id, like_status);

        if (like_status === 'Like'){ 
            like_quantity ++;
            event.target.innerHTML = `&nbsp 👍🏾 &nbsp ${like_quantity}&nbsp`
            event.target.dataset.like_quantity = like_quantity;
            event.target.dataset.like_status = "Cancel_like"

        } else {
            like_quantity --;
            event.target.innerHTML = `&nbsp 👍🏻 &nbsp ${like_quantity}&nbsp`
            event.target.dataset.like_quantity = like_quantity;
            event.target.dataset.like_status = "Like"
        }
        
        if( sibling_dislike_status === 'Cancel_dislike'){
            
            fetch_dislike(post_id, sibling_dislike_status);

            let sibling_dislike_quantity = sibling_thumb_down.dataset.dislike_quantity;
            sibling_dislike_quantity --;
            sibling_thumb_down.innerHTML = `&nbsp 👎🏻 &nbsp ${sibling_dislike_quantity}&nbsp`
            sibling_thumb_down.dataset.dislike_quantity= sibling_dislike_quantity;
            sibling_thumb_down.dataset.dislike_status = "Dislike"
        }
    });
}); 

document.querySelectorAll('.thumb_down').forEach((thumb_down)=>{

    thumb_down.addEventListener('click',(event)=>{

        const post_id = event.target.dataset.post_id;
        const dislike_status=event.target.dataset.dislike_status;
        let dislike_quantity = event.target.dataset.dislike_quantity;
        const sibling_thumb_up = event.target.parentElement.parentElement.firstElementChild.firstElementChild
        const sibling_like_status = sibling_thumb_up.dataset.like_status;

        fetch_dislike(post_id,dislike_status);

        if (dislike_status === 'Dislike'){ 
            dislike_quantity ++;
            event.target.innerHTML = `&nbsp 👎🏾 &nbsp ${dislike_quantity}&nbsp`
            event.target.dataset.dislike_quantity = dislike_quantity;
            event.target.dataset.dislike_status = "Cancel_dislike"

        } else {
            dislike_quantity --;
            event.target.innerHTML = `&nbsp 👎🏻 &nbsp ${dislike_quantity}&nbsp`
            event.target.dataset.dislike_quantity = dislike_quantity;
            event.target.dataset.dislike_status = "Dislike"
        }

        if (sibling_like_status === 'Cancel_like'){

            fetch_like(post_id, sibling_like_status);

            let sibling_like_quantity = sibling_thumb_up.dataset.like_quantity;
            sibling_like_quantity --;
            sibling_thumb_up.innerHTML = `&nbsp 👍🏻 &nbsp ${sibling_like_quantity}&nbsp`
            sibling_thumb_up.dataset.like_quantity = sibling_like_quantity;
            sibling_thumb_up.dataset.like_status = "Like"
        }
    });
}); 

function fetch_like(post_id, like_status){
    fetch('/like',{
            'method'  : 'PUT',
            'body': JSON.stringify({
                post_id: post_id,
                like_status: like_status,
            })
        })
}

function fetch_dislike(post_id,dislike_status){

    fetch('/like',{
            'method'  : 'PUT',
            'body': JSON.stringify({
                post_id: post_id,
                dislike_status: dislike_status,
            })
        })
}