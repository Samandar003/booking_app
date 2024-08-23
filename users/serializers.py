from .models import CustomUserModel
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User=get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user=CustomUserModel.objects.create_user(     
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            city=validated_data['city'],
            municipality=validated_data['municipality'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields="__all__"
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        obj=User.objects.filter(email=attrs['email'])
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}
    
    