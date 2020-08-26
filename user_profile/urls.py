
from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('user/register', views.UserCreateView.as_view(), name='user-registration'),

    path('create', views.UserProfileCreateView.as_view(), name='user-profile-create'),
    path('<int:pk>/detail', views.UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('detail', views.own_user_profile_detail_view, name='own-user-profile-detail'),
    path('<int:pk>/edit', views.UserProfileEditView.as_view(), name='user-profile-edit'),

    path('ajax/follow', views.ajax_follow_create, name='ajax-follow'),
    path('ajax/unfollow', views.ajax_follow_delete, name='ajax-unfollow'),
]
