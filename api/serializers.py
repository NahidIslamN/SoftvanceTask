from rest_framework import serializers
from .models import UserModel, Employer
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = UserModel.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        
        )
        user.set_password(validated_data['password'])
        user.save()
        

        token = Token.objects.create(
            user = user
        )
       
        token.save()
    
        return validated_data
    


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields = ["id","email", "password", "is_superuser", "username",  "first_name", "last_name","date_joined"]



class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employer
        fields = "__all__"