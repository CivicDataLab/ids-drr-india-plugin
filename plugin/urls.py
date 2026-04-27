from django.urls import path

from plugin import views

urlpatterns = [
    path("report", views.generate_report),
]
