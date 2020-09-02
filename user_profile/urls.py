
from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('user/register', views.UserCreateView.as_view(), name='user-registration'),

    path('search', views.user_profile_search_view, name='user-profile-search'),
    path('create', views.UserProfileCreateView.as_view(), name='user-profile-create'),
    path('<int:pk>/detail', views.UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('detail', views.own_user_profile_detail_view, name='own-user-profile-detail'),
    path('<int:pk>/edit', views.UserProfileEditView.as_view(), name='user-profile-edit'),

    path('followed_list', views.user_profile_followed_list_view, name='followed-list'),
    path('<int:pk>/chat', views.chat_main, name='chat'),
    path('<int:pk>/chat/delete', views.delete_chat, name='chat-delete'),
    path('chat_list', views.chat_list, name='chat-list'),

    path('ajax/follow', views.ajax_follow_create, name='ajax-follow'),
    path('ajax/unfollow', views.ajax_follow_delete, name='ajax-unfollow'),
    path('ajax/get_messages', views.ajax_get_chat_messages, name='get-messages')
]
