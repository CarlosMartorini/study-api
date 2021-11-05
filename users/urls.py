from django.urls import path
from .views import Create, Login


urlpatterns = [
    path('accounts/', Create.as_view()),
    path('login/', Login.as_view())
]