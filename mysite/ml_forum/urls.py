from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.ShowSections.as_view(), name='index'),
    re_path(r'^pages/(?P<page>[0-9]{2})/', views.pages),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<slug:username>', views.show_profile, name='profile'),
    path('profile_edit/<slug:username_slug>', views.EditProfile.as_view(), name='profile_edit'),
    path('profile_verify/<slug:username>', views.verify_profile, name='profile_verify'),
    path('section/<int:section_id>', views.ShowTopics.as_view(), name='section'),
    path('section/<int:section_id>/add_topic', views.add_topic, name='add_topic'),
    path('section/<int:section_id>/topic/<int:topic_id>', views.show_topic, name='topic'),
]