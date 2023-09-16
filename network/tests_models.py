import datetime
from django.utils import timezone
from django.test import TestCase


from .models import *


class PostTestCase(TestCase):

    def setUp(self):

        u=User.objects.create(username = "u")   
        p1=Post.objects.create(user = u)
        p2=Post.objects.create(user = u)
        p3=Post.objects.create(user = u)
        
        delta = datetime.timedelta(hours = 5)
        now = timezone.now()

        p1.datetime_editing = now + delta
        p2.datetime_editing = now - delta
        p1.save()
        p2.save()

    def test_valid_post_edited(self):
        p1=Post.objects.get(pk = 1)
        self.assertTrue(p1.post_is_valid())

    def test_invalid_post_edited(self):
        p2=Post.objects.get(pk = 2)
        self.assertFalse(p2.post_is_valid())

    def test_valid_post_not_edited(self):
        p3=Post.objects.get(pk = 3)
        self.assertTrue(p3.post_is_valid())

class CommentTestCase(TestCase):

    def setUp(self):
        u=User.objects.create(username = "u")   
        p=Post.objects.create(user = u)

        delta = datetime.timedelta(hours = 5)
        now = timezone.now()

        c1 = Comment.objects.create(user = u, post = p)
        c1.datetime = now + delta
        c1.save()
       
        c2 = Comment.objects.create(user = u, post = p)
        c2.datetime = now - delta
        c2.save()

    def test_valid_comment(self):
        c1 = Comment.objects.get(pk=1)
        self.assertTrue(c1.comment_is_valid())

    def test_invalid_comment(self):
        c2 = Comment.objects.get(pk=2)
        self.assertFalse(c2.comment_is_valid()) 

      

