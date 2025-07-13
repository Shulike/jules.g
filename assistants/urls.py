from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssistantListView.as_view(), name='assistant_list'),
    path('create/', views.create_assistant, name='create_assistant'),
]
