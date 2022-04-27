from django.urls import path
from todos.views import CreateListAPIView,RUDAPIView


urlpatterns = [
    # path('createTodo',CreateTodoAPIView.as_view(),name='createTodo'),
    # path('list',TodoListAPIView.as_view(),name='list'),
    path('',CreateListAPIView.as_view(),name='todosCR'),
    path('<int:id>',RUDAPIView.as_view(),name='todoRUD'),
]