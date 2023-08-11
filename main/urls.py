from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "main"
urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('settings', views.settings, name='settings'),

    path('login_view', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('logout_view', views.logout_view, name='logout_view'),

    path('delete/<int:pk>/<str:option>', views.delete, name='delete'),

    path('building/<int:pk>', views.building, name='building'),
    path('class_view/<str:name>', views.class_view, name='class'),

    path('create_teacher/<str:name>', views.create_teacher, name='create_teacher'),
    path('all_teachers/', views.all_teachers, name='all_teachers'),
    path('teacher/<int:pk>', views.teacher, name='teacher'),

    path('create_student/', views.create_student, name='create_student'),
    path('all_students/', views.all_students, name='all_students'),
    path('student/<int:pk>', views.student, name='student'),

    path('nextYear/', views.nextYear, name='nextYear'),
    path('train/<int:pk>', views.train, name='train'),
]
