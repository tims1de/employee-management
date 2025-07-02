from django.contrib import admin
from django.urls import path

from employees import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_info/', views.get_all_employees_info),
    path('info_by_level/', views.get_employees_by_similar_level)
]
