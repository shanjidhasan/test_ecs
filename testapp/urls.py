from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('health', views.health, name='health'),
    path('test/hello', views.test_hello, name='test_hello'),
    path('test/json', views.test_json, name='test_json'),
    path('test/db', views.test_db, name='test_db'),
]
