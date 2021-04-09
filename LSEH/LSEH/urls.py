from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contents/', include('contents.urls')),
    path('accounts/', include('accounts.urls')),
]
