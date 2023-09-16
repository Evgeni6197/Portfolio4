import datetime
from django.utils import timezone

from django.test import TestCase, Client

from .models import *
from .helper import *

class LikeViewTestCase(TestCase):

    def test_put_request(self):

        w=User.objects.create(username = 'w')
        p = Post.objects.create(user = w)

        c = Client()
        c.force_login(w)

        response = c.put('/like', data = b'{"post_id":"1","like_status":"Like"}')
        l=Like.objects.get(pk=1)
        self.assertEqual(l.user.username,'w','fails put request in Like case' )
        self.assertEqual(response.status_code, 204, 'wrong status code in Like case')

        response = c.put('/like', data = b'{"post_id":"1","like_status":"Cancel_like"}')
        self.assertEqual(Like.objects.all().count(), 0, 'fails put request  in Cancel_like case')
        self.assertEqual(response.status_code, 204, 'wrong status code in Cancel_like case')

        response = c.put('/like', data = b'{"post_id":"1","dislike_status":"Dislike"}')
        d=Dislike.objects.get(pk=1)
        self.assertEqual(d.user.username,'w','fails put request in Dislike case' )
        self.assertEqual(response.status_code, 204, 'wrong status code in Dislike case')

        response = c.put('/like', data = b'{"post_id":"1","dislike_status":"Cancel_dislike"}')
        self.assertEqual(Dislike.objects.all().count(), 0, 'fails put request  in Cancel_dislike case')
        self.assertEqual(response.status_code, 204, 'wrong status code in Cancel_dislike case')

class New_postViewTestCase(TestCase):

    def test_post_request(self):

        w=User.objects.create(username = 'w')

        c = Client()
        c.force_login(w)

        response = c.post('/new_post/2/0/all_posts', {'content':'post content'})
        self.assertEqual(response.status_code, 302, 'wrong status code')
        self.assertEqual(Post.objects.get(pk=1).content, 'post content', 'error in put request processing')


class Edit_postViewTestCase(TestCase):

    def test_put_request(self):

        u=User.objects.create(username = 'u')
        w=User.objects.create(username = 'w')
        Post.objects.create(user = w, content = 'previous content')

        c = Client()
        c.force_login(w)  


        # checks post content update 
        response = c.put('/edit_post/0', data = b'{"post_id":"1","new_content":"new edited content"}')
        self.assertEqual(response.status_code, 204, 'wrong status code in put request')

        edited_post_content = Post.objects.get(pk=1).content
        self.assertEqual(edited_post_content, "new edited content", 'error in put request')

        c.logout()
        c.force_login(u)

        # checks defense from unauthorized editing
        # test leads to printing  out "Not authorized editing attempt" message
        # by edit_post view
        response = c.put('/edit_post/0', data = b'{"post_id":"1","new_content":"unauthorized editing attempt"}')
        edited_post_content = Post.objects.get(pk=1).content
        self.assertEqual(edited_post_content, "new edited content", 'erroneous disabled unauthorized editing defense ')

    def test_get_request(self):

        datetime_creation = timezone.now()
        datetime_editing = datetime_creation + datetime.timedelta(minutes = 10)

        w=User.objects.create(username = 'w')
        Post.objects.create(user = w, datetime_editing = datetime_editing )

        c = Client()
        c.force_login(w) 

        # checks JsonResponse 
        response = c.get('/edit_post/1')
        self.assertEqual(response.status_code, 200, 'wrong status code in get request')

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"datetime_editing": convert_datetime_format(datetime_editing), "post_id": 1})

class FollowViewTestCase(TestCase):

    def test_follow_unfollow(self):
        u=User.objects.create(username = 'u')
        w=User.objects.create(username = 'w')

        c = Client()
        c.force_login(w) 

        # checks follow action
        response = c.post('/follow/1/2', {"action":'follow'})
        f=Follower.objects.get(pk =1)
        self.assertEqual(f.follower, w, 'wrong follow action')
        self.assertEqual(f.followed, u, 'wrong follow action')
        self.assertEqual(response.status_code, 302, 'wrong status code in follow action')


        # checks unfollow action
        response = c.post('/follow/1/2', {"action":'unfollow'})
        count = Follower.objects.all().count()
        self.assertEqual(count, 0, 'wrong unfollow action')
        self.assertEqual(response.status_code, 302, 'wrong status code in follow action')