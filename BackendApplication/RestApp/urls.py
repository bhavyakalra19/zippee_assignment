from django.urls import path
from RestApp.views import *

#restapp urls; these is included in main urls.py
urlpatterns = [
    path('tasks/', TaskModelView.as_view(), name='tasks-view'),
    path('tasks/<int:pk>/', TaskModelView.as_view(), name='tasks-view'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('tasks/completed/', TaskModelCompletedView.as_view(), name="filer_completed")
]