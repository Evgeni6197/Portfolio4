from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    # poster
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="my_posts")
    content = models.TextField(blank=True)

    # auto filling on instantiation
    datetime_creation = models.DateTimeField(auto_now_add=True)

    # time of last editing
    datetime_editing = models.DateTimeField(null = True, blank = True)

    def post_is_valid(self):
        if self.datetime_editing:
            return self.datetime_editing > self.datetime_creation
        else:
            return True

class Like(models.Model):
    # like author
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_likes")

    # like target
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes" ) 

class Follower(models.Model):
    # who followes
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_I_am_following")

    # who is followed
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_followers")

class Comment(models.Model):
    # comment author
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")

    # comment target
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments" )

    # auto filling on instantiation
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

    def comment_is_valid(self):
        if self.datetime > self.post.datetime_creation:
            return True
        else:
            return False

class Dislike(models.Model):
    # dislike author
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_dislikes")

    # dislike target
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="dislikes" ) 