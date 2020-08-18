
from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('<int:pk>/detail', views.UserProfileDetail.as_view(), name='user_profile'),
]
