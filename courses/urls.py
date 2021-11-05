from django.urls import path
from .views import View, ViewById, Create


urlpatterns = [
    path('courses/', View.as_view()),
    path('courses/<int:course_id>', ViewById.as_view()),
    path('courses/<int:course_id>/registrations', Create.as_view()),
]