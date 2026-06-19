from django.urls import path
from . import api

urlpatterns = [
    path('tool-config/<str:tool_name>/', api.tool_config, name='tool_config'),
    path('tools/<str:tool_name>/', api.tool_execute, name='tool_execute'),
]
