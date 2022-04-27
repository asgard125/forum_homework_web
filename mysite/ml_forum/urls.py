from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.ShowSections.as_view(), name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<slug:username>', views.ShowProfile.as_view(), name='profile'),
    path('profile_edit/<slug:username_slug>', views.EditProfile.as_view(), name='profile_edit'),
    path('profile_verify/<slug:username>', views.verify_profile, name='profile_verify'),
    path('section/<int:section_id>', views.ShowTopics.as_view(), name='section'),
    path('section/<int:section_id>/add_topic', views.add_topic, name='add_topic'),
    path('section/<int:section_id>/topic/<int:topic_id>', views.ShowTopicPosts.as_view(), name='topic'),
    path(r'section/<int:section_id>/topic/<int:topic_id>/add_post/<str:reply_to>', views.AddPost.as_view(), name='add_post'),
    path(r'section/<int:section_id>/topic/<int:topic_id>/add_post', views.AddPost.as_view(), name='add_post', kwargs={'reply_to':' '}),
    path('section/<int:section_id>/topic/<int:topic_id>/post_edit/<int:post_id>', views.EditPost.as_view(), name='edit_post'),
    path('section/<int:section_id>/topic/<int:topic_id>/post_delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('<slug:username>/replies', views.ShowReplies.as_view(), name='replies'),
    path('reply_watched/<int:post_id>', views.reply_watched, name='reply_watched'),
]