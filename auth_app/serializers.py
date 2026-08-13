from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


User = get_user_model()

class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        style={'input_type':'password'}
    )
    password_confirmation = serializers.CharField(
        write_only = True,
        style={'input_type':'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirmation' ]
        extra_kwargs = {
            'email' : {'required' : True},
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
                        }

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email__iexact=value):
            raise serializers.ValidationError(
                'This Email already Exists'
            )
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password  = attrs.pop('password_confirmation')

        if password != confirm_password:
            raise serializers.ValidationError(
             {  'password_confirmation' : 'The passwords do not match'}
            )
        
        return attrs

    def create(self, validated_data):

        password = validated_data.pop('password')

        new_user = User.objects.create_user(
            password = password,
            **validated_data
        )
        return new_user

class LoginSerializer(serializers.Serializer):

    identifier = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        identifier = attrs['identifier']
        password = attrs['password']

        user =  User.objects.filter(email__iexact = identifier ).first()

        if not user:
            user =  User.objects.filter(username__iexact = identifier ).first()


        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid Credentials')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
            'user' : {
                'id' : user.id,
                'email' : user.email,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
            },
        }

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class UpdateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']