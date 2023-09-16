import datetime
from django.utils import timezone
from django.test import TestCase, Client

from .models import *

class IndexViewTestCase(TestCase):

    def setUp(self):
        
        u=User.objects.create(username = 'u')
        w=User.objects.create(username = 'w')
        x=User.objects.create(username = 'x')
        y=User.objects.create(username = 'y')

        for i in range (1,12):
            delta = datetime.timedelta(minutes = i)
            p = Post.objects.create(user = u)
            p.datetime_creation += delta
            p.save()

        for i in range (12,18):
            delta = datetime.timedelta(minutes = i)
            p = Post.objects.create(user = x)
            p.datetime_creation += delta
            p.save()

        for i in range (18,23):
            delta = datetime.timedelta(minutes = i)
            p = Post.objects.create(user = y)
            p.datetime_creation += delta
            p.save()

        for i in range (23,26):
            delta = datetime.timedelta(minutes = i)
            p = Post.objects.create(user = w)
            p.datetime_creation += delta
            p.save()


    def test_reverse_chronological_order_output(self):

        c=Client()

        # all_post case
        response = c.get('/1/0/all_posts')
        page_obj = response.context['posts']
        self.assertGreater(page_obj[0][0].datetime_creation, page_obj[-1][0].datetime_creation, 'fails output order in all_posts')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        # profile case - profile owner user u
        response = c.get('/1/1/profile')
        page_obj = response.context['posts']
        self.assertGreater(page_obj[0][0].datetime_creation, page_obj[-1][0].datetime_creation, 'fails output order in profile')
        self.assertEqual(response.status_code, 200, 'wrong status code')

    def test_pagination(self): 

        c=Client()

        # all post case 
        response = c.get('/3/0/all_posts')
        page_obj = response.context['posts']
        num_pages = response.context['num_pages']
        self.assertEqual(len(page_obj),5, 'fails last output page post quantity in all_posts')
        self.assertEqual(num_pages,3,'fails pagination quantity in all_posts')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        # profile case - profile owner user u
        response = c.get('/2/1/profile')
        page_obj = response.context['posts']
        num_pages = response.context['num_pages']
        self.assertEqual(len(page_obj),1, 'fails last output page post quantity in profile user u')
        self.assertEqual(num_pages,2,'fails pagination quantity in profile user u')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        # profile case - profile owner user w
        response = c.get('/1/2/profile')
        page_obj = response.context['posts']
        num_pages = response.context['num_pages']
        self.assertEqual(len(page_obj),3, 'fails last output page quantity in profile user w')
        self.assertEqual(num_pages,1,'fails pagination quantity in profile user w')
        self.assertEqual(response.status_code, 200, 'wrong status code')

    def test_buttons(self):    
        
        w=User.objects.get(username='w')
        u=User.objects.get(username='u')

        c=Client()
        c.force_login(w)

        # w followers u
        f=Follower.objects.create(follower = w, followed = u)        
        response = c.get('/1/1/profile')
        button_follow = response.context['button_follow']
        button_unfollow = response.context['button_unfollow']  
        self.assertFalse(button_follow, 'fails button_follow definition in already followed case')
        self.assertTrue(button_unfollow, 'fails button_unfollow definition in already followed case')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        # w does not follower u
        f.delete()
        response = c.get('/1/1/profile')
        button_follow = response.context['button_follow']
        button_unfollow = response.context['button_unfollow']
        self.assertTrue(button_follow, 'fails button_follow definition in not followed case')
        self.assertFalse(button_unfollow, 'fails button_unfollow definition in not followed case')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        c.logout()
        response = c.get('/1/1/profile')
        button_follow = response.context['button_follow']
        button_unfollow = response.context['button_unfollow']
        self.assertFalse(button_follow, 'fails button_follow definition in non-authenticated')
        self.assertFalse(button_unfollow, 'fails button_unfollow definition in non-authenticated')
        self.assertEqual(response.status_code, 200, 'wrong status code')

    def test_following(self):
        
        u=User.objects.get(username='u')
        w=User.objects.get(username='w')
        x=User.objects.get(username = 'x')
        y=User.objects.get(username = 'y')

        f_w_x = Follower.objects.create(follower = w, followed = x)
        f_w_y = Follower.objects.create(follower = w, followed = y)
        f_u_w = Follower.objects.create(follower = u, followed = w)

        c = Client()
        c.force_login(w)

        # profile case - profile owner user w
        # check number of followers and followed
        response = c.get('/1/2/profile')
        followers = response.context['followers']
        followed = response.context['followed']

        self.assertEqual(followers, 1, 'fails followers quantity in profile')
        self.assertEqual(followed, 2, 'fails followed quantity in profile')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        #following case - checks the total number of posts of users, followed by the user logged in
        response = c.get('/1/0/following')
        num_pages = response.context['num_pages']
        self.assertEqual(num_pages, 2, 'fails output page quantity in following case')

        # check reverse chronological order in following case
        page_obj = response.context['posts']
        self.assertGreater(page_obj[0][0].datetime_creation, page_obj[-1][0].datetime_creation, 'fails output order in following')
        self.assertEqual(response.status_code, 200, 'wrong status code')

        # check quantity of posts in the last output page in following case
        response = c.get('/2/0/following')
        page_obj = response.context['posts']
        self.assertEqual(len(page_obj),1, 'fails last output page post quantity in following')
        self.assertEqual(response.status_code, 200, 'wrong status code')