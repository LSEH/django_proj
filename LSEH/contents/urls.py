from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('delete/<int:content_id>/', views.delete, name='delete'),
    path('update/<int:content_id>/', views.update, name='update'),
    path('detail/<int:content_id>/', views.detail, name='detail'),
    path('create_comment/<int:content_id>/', views.create_comment, name='create_comment'),
    path('delete/<int:content_id>/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like/contents/<int:content_id>/', views.like_contents, name='like_contents'),
    path('like/contents/<int:content_id>/comments/<int:comment_id>/', views.like_comments, name='like_comments'),
    path('create/<int:content_id>/review/', views.create_review, name='create_review'),
    path('delete/<int:content_id>/review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('update/<int:content_id>/review/<int:review_id>/', views.update_review, name='update_review'),
    path('see_later/<int:content_id>/review/<int:review_id>/', views.see_later, name='see_later'),
    path('like/<int:content_id>/review/<int:review_id>/', views.like_reviews, name='like_reviews'),
    path('watch/<int:content_id>/review/<int:review_id>/', views.watch_reviews, name='watch_reviews'),
]
