from django.urls import path
from .views import View, ViewById, Create, SubmissionView, ListSubmissions


urlpatterns = [
    path('activities/', View.as_view()),
    path('activities/<int:activity_id>/', ViewById.as_view()),
    path('activities/<int:activity_id>/submissions/', Create.as_view()),
    path('submissions/<int:submission_id>/', SubmissionView.as_view()),
    path('submissions/', ListSubmissions.as_view()),
]