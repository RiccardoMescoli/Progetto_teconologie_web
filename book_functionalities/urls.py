from django.urls import path
from book_functionalities import views

app_name = 'book_functionalities'

urlpatterns = [
    path('author/<int:pk>/detail', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/edit', views.AuthorEditView.as_view(), name='author-edit'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),
]