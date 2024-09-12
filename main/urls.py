from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),

    path('user_signup',views.user_signup,name='user_signup'),

    path('user_login',views.user_login,name='user_login'),

    path('user_logout',views.user_logout,name='user_logout'),

    path('delete_user',views.delete_user,name='delete_user'),

    path('new_post',views.new_post,name='new_post'),

    path('delete_post/<int:post_id>',views.delete_post,name='delete_post'),

    path('edit_post/<int:post_id>',views.edit_post,name='edit_post'),

    path('error404',views.error404),

]