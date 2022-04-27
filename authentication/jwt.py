from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings
from rest_framework import exceptions
import jwt
from authentication.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        auth_data = auth_header.decode("utf-8")

        auth_data_splited = auth_data.split(" ")

        if len(auth_data_splited) != 2:
            raise exceptions.AuthenticationFailed("Invalid Token")

        token = auth_data_splited[1]

        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms = "HS256")

            username = payload["username"]

            user = User.objects.get(username = username)

            return (user,token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed("Expired Token, Login Again")

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed("Invalid Token")

        except User.DoesNotExist as ex:
            raise exceptions.AuthenticationFailed("User Doesnt Exist please register")


        return super().authenticate(request)