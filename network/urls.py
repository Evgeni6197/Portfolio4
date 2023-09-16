
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:num_page>',views.index, name='index'),
    path('<int:num_page>/<int:profile_owner_id>/<str:flag>',views.index, name='index'),
    path('new_post/<int:next_page>/<int:profile_owner_id>/<str:flag>',views.new_post,name='new_post'),
    path('edit_post/<int:post_id>',views.edit_post,name='edit_post'),
    path('get_comments/<int:post_id>',views.get_comments, name='get_comments'),
    path('new_comment',views.new_comment,name = 'new_comment'),
    path('like',views.like, name = 'like' ),
    path('follow/<int:profile_owner_user_id>/<int:next_page>',views.follow, name = 'follow'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<path:x>',views.message, name = 'message')
]
