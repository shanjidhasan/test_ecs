from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('test/hello/', views.test_hello, name='test_hello'),
    path('test/json/', views.test_json, name='test_json'),
]
