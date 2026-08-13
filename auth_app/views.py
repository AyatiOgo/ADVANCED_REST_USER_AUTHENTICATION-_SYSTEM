from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import ( UserRegistrationSerializer, 
                          LoginSerializer, 
                          UserProfileSerializer, UpdateUserProfileSerializer)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer( data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer( data = request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request, id):
        User = get_user_model()
        user = User.objects.get(id=id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        User = get_user_model()
        user = User.objects.get(id=id)

        if not request.user.is_authenticated:
            return Response({'Authentication_error':'Login credentials Not found'}, status=status.HTTP_400_BAD_REQUEST)

        if user.id != request.user.id:
            return Response({'Unauthorized':'User Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        serializer =  UpdateUserProfileSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)