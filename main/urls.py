from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "main"
urlpatterns = [
    path('', views.home, name='home'),

    path('login_view', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('logout_view', views.logout_view, name='logout_view'),

    path('create', views.create, name='create'),

    path('building/<int:pk>', views.building, name='building'),
    path('class_view/<str:name>', views.class_view, name='class'),
    path('faculty/<int:pk>', views.faculty, name='faculty'),
    path('student/<int:pk>', views.student, name='student'),
]
