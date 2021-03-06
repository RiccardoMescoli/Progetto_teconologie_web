"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from book import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('activity_feed', views.activities_feed_view, name='activity_feed'),
    path('personalized_recommendations', views.personalized_recommendations_view, name='personalized_recommendations'),

    path('user_profile/', include('user_profile.urls')),
    path('user/login', auth_views.LoginView.as_view(), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),

    path('book_functionalities/', include('book_functionalities.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
