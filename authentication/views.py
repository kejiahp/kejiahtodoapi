from urllib import response
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication import serializer
import authentication
from authentication.serializer import RegisterSerializers,LoginSerializer
from rest_framework import response,status,permissions
from django.contrib.auth import authenticate

class RegisterAPIView(GenericAPIView):
    authentication_classes = []

    serializer_class = RegisterSerializers


    def post(self,request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status = status.HTTP_201_CREATED)

        return response.Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self,request):
        email = request.data.get("email",None)
        password =request.data.get("password",None)

        user = authenticate(username = email, password = password)

        if user:
            serializers = self.serializer_class(user)

            return response.Response(serializers.data, status=status.HTTP_200_OK)

        return response.Response({"message":"Invalid Credentials, try again"}, status = status.HTTP_401_UNAUTHORIZED)

class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        user = request.user

        serializers = RegisterSerializers(user)

        return response.Response({"user":serializers.data})