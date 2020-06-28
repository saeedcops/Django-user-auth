from django.conf.urls import url
from auth_app import views

app_name = 'auth_app'

urlpatterns = [
    url('register/', views.register, name='register'),
    url('user_login/', views.user_login, name='user_login')
]
