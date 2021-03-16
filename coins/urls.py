from django.urls import path
from .views import *

app_name = 'coins'

urlpatterns = [
    path('', view=FileView.as_view(),
         name='main'),
]
