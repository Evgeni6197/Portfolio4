import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
from .helper import *

PAGINATION = 10

def index(request, num_page=1, profile_owner_id = 0, flag ='all_posts' ):
    '''
    Renders "PAGINATION" number of posts. 
    num_page - int - serial number of rendered collection in the total number of posts to render
                    in accordance with the flag value
    profile_owner_id - int - 0 for flag = 'all_posts' and flag = 'following' and equals to user id
                            in case when flag = 'profile'. 

    flag - str - 'all-posts' -  in general case
               -  'following' - case when the view renders collection of posts, written by users
                                followed by the current  logged in user. This takes place on clicking upon 
                                "Following" link on top of the template
               -  'profile'   - case when the view renders posts,  written by the current  logged in user
                                This takes place on clicking upon the username in template
    '''

    profile_owner_username = profile_owner_email = ''
    followers_count=followed_count=0
    button_follow =  button_unfollow = False

    if flag == 'all_posts':
        posts=Post.objects.order_by('-datetime_creation').all()
    elif flag == 'profile':
        posts = Post.objects.order_by('-datetime_creation').filter(user = profile_owner_id)
        try:
            profile_owner = User.objects.get(pk=profile_owner_id )
            profile_owner_username = profile_owner.username
            profile_owner_email = profile_owner.email
            followers_count = profile_owner.my_followers.count()
            followed_count = profile_owner.who_I_am_following.count()
        except:
            # Case of malicious client side editing or wrong typing in to the url browser field
            print('error while getting profile_owner from User model')
            return HttpResponseRedirect(reverse('message', args = 'x'))

        # if user is logged in and profile_owner  is valid
        if request.user.is_authenticated and profile_owner_username:
            try:
                temp = Follower.objects.filter(follower = request.user, followed = profile_owner_id).count()
                if temp > 0: # user logged in already follows after  profile_owner# user logged in already follows after  profile_owner
                    button_follow = False
                    button_unfollow = True
                else:
                    button_follow = True
                    button_unfollow = False 
                
            except:
                print('error in Follower db') 
                return HttpResponseRedirect(reverse('message', args = 'w'))         

    elif flag == 'following' and request.user.is_authenticated:

        followed_id_s =[]
        for follower_obj in request.user.who_I_am_following.all():
            followed_id_s.append(follower_obj.followed.id)    
        
        posts =[]
        for followed_id in followed_id_s:
            posts_of_one_followed = Post.objects.filter(user = followed_id)
            for post in posts_of_one_followed:
                posts.append(post)
   
        posts.sort( key = lambda post: post.datetime_creation, reverse=True)

    else:
       return HttpResponseRedirect(reverse("index")) 


    # posts_plus is a list of tuples; these tuples  contain posts themselves and some additions. 
    # PAGINATION quantity of posts_plus  elements will be rendered
    posts_plus =[]
    for post in posts:
        if request.user.is_authenticated:
            # my_like_is_given and my_dislike_is_given equal
            # 1 if user logged in already made like or dislike on this particular post, 0 otherwise 
            my_like_is_given = Like.objects.filter(user = request.user, post=post).count()
            my_dislike_is_given = Dislike.objects.filter(user = request.user, post=post).count()
            posts_plus.append((post, post.likes.count(), my_like_is_given, post.id, post.dislikes.count(), my_dislike_is_given,))
            
        else:
            posts_plus.append((post, post.likes.count(), -1, post.id, post.dislikes.count(), -1, ))
        
    paginator = Paginator(posts_plus, PAGINATION)
    num_pages = paginator.num_pages
    if 0 < num_page <= num_pages:
        page_obj = paginator.get_page(num_page)
    else:
        # Case of malicious client side editing or wrong typing in to the url browser field
        print(' page with such number does not exist in pagination object')
        return HttpResponseRedirect(reverse('message', args = 'x')) 

    form = New_post()
    
    return render(request, "network/index.html",{
        "posts": page_obj,
        "num_pages": num_pages,
        'next_page': num_page + 1,
        'prev_page': num_page - 1,
        'form': form,
        'flag': flag,
        'profile_owner_id': profile_owner_id,
        'profile_owner_username': profile_owner_username,
        'profile_owner_email' :  profile_owner_email,
        'followers': followers_count ,
        'followed': followed_count,
        'button_follow': button_follow ,
        'button_unfollow': button_unfollow,
        'username':request.user.username
    })

@csrf_exempt
@login_required(login_url="/login")
def like(request):
    '''
    Changes database on getting PUT data
    '''
    if request.method == "PUT":

        data = json.loads(request.body)
        flag =''

        try:
            post_id = data['post_id']
            if data.get('like_status') is not None:
                like_status = data['like_status']
                flag='like'
            if data.get('dislike_status') is not None:    
                dislike_status = data['dislike_status']
                flag = 'dislike'
            post = Post.objects.get(pk=post_id)
        except:
            # case of malicious client side edition
            print("Error while fetch like/dislike")
            return HttpResponse(status=204)

        if flag == 'like':
            if like_status == "Cancel_like":
                try:
                    like = Like.objects.get(user = request.user, post = post)
                except:
                    print ('Error while getting Like object' )
                    return HttpResponse(status=204)
                like.delete()            
            elif like_status == "Like":

                like = Like(user = request.user, post = post)
                like.save()
            else:
                raise Exception ('Invalid like_status parameters on like/dislike fetching')
        elif flag == 'dislike':
            if dislike_status == "Cancel_dislike":
                try:
                    dislike = Dislike.objects.get(user = request.user, post = post)
                except:
                    raise Exception ('Error while getting Dislike object' )
                    return HttpResponse(status=204)
                dislike.delete()            
            elif dislike_status == "Dislike":

                dislike = Dislike(user = request.user, post = post)
                dislike.save()
            else:
                raise Exception ('Invalid dislike_status parameters on like/dislike fetching')
        else:
            raise Exception("Error while fetch like/dislike")
            return HttpResponse(status=204) 

    return HttpResponse(status=204)

@login_required(login_url="/login")
def new_post(request, next_page, profile_owner_id , flag):
    '''
    Receives POST data and records it to db
    arguments are not processed here and are directly passed to the "index" view
    '''
    num_page =  next_page - 1

    if request.method == 'POST':

        form = New_post(request.POST)
        try:
            if form.is_valid():
                content = form.cleaned_data['content']
                new_post = Post(user = request.user, content = content)
                new_post.save()

                return HttpResponseRedirect(reverse("index", args = (num_page, profile_owner_id , flag)))
            else:
                # case of malicious client side editing
                raise Exception ("Invalid form")
        except:
            print("Invalid form in new_post view")
            return HttpResponseRedirect(reverse("index")) 
    else:    
        
        return HttpResponse(status=204)

@csrf_exempt
@login_required(login_url="/login")
def edit_post(request,post_id):
    '''
    Receives PUT data for post editing
    Edits post with id = post_id (<int>)  
    Checks if the user logged in really is the author of the post
    Creates  editing datetime
    Makes a db record
    
    If request.method == "GET" - retrieves db data
    Converts editing datetime to the format
    Similar to template datetime creation format
    '''

    if request.method == "PUT":

        data = json.loads(request.body)

        try:
            post_id = data['post_id']
            new_content = data['new_content']
        except :
            print("Invalid PUT data in edit_post view")
            return HttpResponse(status=204) 

        try:
            post = Post.objects.get(pk=post_id)
        except:
            print("post does not exist")
            return HttpResponse(status=204) 
        
        if post.user != request.user:
            print('Not authorized editing attempt')
            return HttpResponse(status=204) 


        post.datetime_editing = timezone.now()
        post.content = new_content
        post.save() 

    elif request.method == "GET":
        
        try:
            post = Post.objects.get(pk=post_id)
        except:
            print("wrong post_id in GET method")
            return HttpResponse(status=204) 

        datetime_editing = convert_datetime_format(post.datetime_editing)

        return JsonResponse({"datetime_editing": datetime_editing, 'post_id':post_id})
        
    return HttpResponse(status=204)  


def get_comments(request, post_id):
    '''
    Retrieves comments for post with id=post_id (<int>) from db
    As well as initial post data
    Converts data to format ready for HTML rendering
    '''
   
    if request.method == 'GET':

        try:
            post = Post.objects.get(pk=post_id)
            comments = Comment.objects.order_by('-datetime').filter(post = post)
        except:
            print('Not valid post id')
            return JsonResponse({"success":False})
        comments_list = []
        for comment in comments:
            comments_list.append(f'<i>{comment.datetime.strftime("%d/%m/%Y %H:%M  ")}</i>&nbsp;&nbsp<strong>{comment.user.username}</strong>:&nbsp;&nbsp;{comment.content} ')
        
        
        initial_post = f'<strong>{post.user.username}</strong>:&nbsp;&nbsp;{post.content} '

        return JsonResponse({"success":True, "post_content":initial_post, "comments":comments_list})
    
    return HttpResponse(status=204)

@csrf_exempt
@login_required(login_url="/login")
def new_comment(request):
    """
    Records new comment to db
    """

    if request.method == 'PUT':

        data = json.loads(request.body)

        try:
            post_id = int(data['post_id'])
            content = data['new_comment_content']
            post = Post.objects.get(pk = post_id)
        except:
            print('Error on PUT data in new_comment_views')
            return HttpResponse(status=204)
        new_comment = Comment(user = request.user, post = post, content = content)
        new_comment.save()

    return HttpResponse(status=204)


@login_required(login_url="/login")
def follow(request, profile_owner_user_id, next_page):
    '''
    Receives POST data and modifies db
    parameters : profile_owner_user_id - <int> - target user to follow/unfollow
                 next_page  - <int>  - parameter to pass to "index" view
    '''
   
    if request.method == 'POST':   
        try:
            action = request.POST['action']
            profile_owner = User.objects.get(pk = profile_owner_user_id)
        except:
            #case of malicious client side editing
            print('invalid POST request in "follow" view')
            return HttpResponseRedirect(reverse('message', args = 'w'))

        if action == 'follow':
            # if user logged in try to follow not himself and he does not yet follows profile_owner 
            if request.user.id != profile_owner_user_id and not Follower.objects.filter(follower = request.user, followed = profile_owner).count():    
                Follower(follower = request.user, followed = profile_owner).save()
            else:
                print('invalid profile_owner_user_id in follow view or erroneous doubling follower object')
                return HttpResponseRedirect(reverse('message', args = 'w'))

        elif action == 'unfollow': 
            try:
                follower = Follower.objects.filter(follower = request.user, followed = profile_owner)[0]
                follower.delete()
            except:
                #case of malicious client side editing
                print('follower object does not exist ')
                return HttpResponseRedirect(reverse('message', args = 'w'))
        else:
            #case of malicious client side editing
            return HttpResponseRedirect(reverse('message', args = 'w'))

        return HttpResponseRedirect(reverse('index', args = (next_page - 1, profile_owner_user_id, 'profile') ))

    else:
        return HttpResponseRedirect(reverse('message', args = 'x'))

def login_view(request):
    if request.method == "POST":

        try:
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
        except:
            #case of malicious client side editing
            return HttpResponseRedirect(reverse('message', args = 'w'))

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
        except:
            #case of malicious client side editing
            print('Error in POST parameters in register view')
            return render(request, "network/register.html")

        if len(username)>50:
            return render(request, "network/register.html", {
                "message": "Too long username."
            })

        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        if not username.strip():
            return render(request, "network/register.html", {
                "message": "Username must not be empty."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def message(request,x):

    if x == 'w':
        message = ' Something went wrong - try again'
    else:
        message = "404 Not Found"

    return render(request, 'network/message.html',{

        "message":message
    })
