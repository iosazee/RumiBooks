from django.urls import path
from .views import home, privacy

urlpatterns = [
    path('', home, name="home"),
    path('privacy/', privacy, name="privacy"),
]