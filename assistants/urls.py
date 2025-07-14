from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssistantListView.as_view(), name='assistant_list'),
    path('create/', views.create_assistant, name='create_assistant'),
    path('<int:assistant_id>/chat/', views.ChatView.as_view(), name='chat'),
]
