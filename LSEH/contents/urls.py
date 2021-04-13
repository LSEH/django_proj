from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('detail/<int:content_id>/', views.detail, name='detail'),
    path('update/<int:content_id>/', views.update, name='update'),
    path('delete/<int:content_id>', views.delete, name='delete'),
    path('create_comment/<int:content_id>', views.create_comment, name='create_comment'),
]
