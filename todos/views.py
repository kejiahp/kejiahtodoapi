from cgitb import lookup
import imp
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import permissions,filters
from todos.serializer import TodoSerializer
from todos.models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from todos.pagination import CustomPageNumberPagination

#CREATING A VIEW THAT HANDLES BOTH GET TODOS AND CREATE TODOS
class CreateListAPIView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    pagination_class = CustomPageNumberPagination


    filterset_fields = ['id','title','desc','is_complete']
    search_fields = ['id','title','desc','is_complete']
    ordering_fields = ['id','title','desc','is_complete']


    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner = self.request.user)

#CREATING A VIEW THAT PERFORMS THE R.U.D ACTIONS ON A SINGLE MODEL OBJECT
class RUDAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Todo.objects.filter(owner = self.request.user)



# class CreateTodoAPIView(CreateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = TodoSerializer

#     def perform_create(self, serializer):
#         return serializer.save(owner = self.request.user)

# class TodoListAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         return Todo.objects.filter(owner = self.request.user)