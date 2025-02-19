from django.contrib import admin
from django.urls import path,include
from home import views
from .views import ask_ai
urlpatterns = [
    path('',views.index,name='Home'),
    path("api/ask/", ask_ai, name="ask_ai"),  # AI Assistant API
]
