from rest_framework import serializers
from authentication.models import User

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 6, max_length = 20, write_only = True)

    class Meta:
        model = User
        fields = ('username','email','password',)
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 6, max_length = 20, write_only = True)

    class Meta:
        model = User
        fields = ('email','username','password','token',)

        read_only_fields = ["token"]