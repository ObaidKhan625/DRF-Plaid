from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('Task.urls', 'Task'), namespace='Task')),
    path('admin/', admin.site.urls),
]
