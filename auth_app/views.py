from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import ( UserRegistrationSerializer, 
                          LoginSerializer, 
                          UserProfileSerializer, UpdateUserProfileSerializer)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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


# class VerifyEmailView(APIView):

#     def get(self, request, uid, token):
#         User = get_user_model()

#         try:
#             user_id = force_str(  urlsafe_base64_decode(uid))
#             user = User.objects.get( id=user_id )

#         except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#             return Response({"detail":"Invalid verification link."},
#                                 status=status.HTTP_400_BAD_REQUEST)

#         if not default_token_generator.check_token(user,token):
#             return Response({ "detail":"Invalid or expired verification link."},
#                             status=status.HTTP_400_BAD_REQUEST )

#         if user.email_verified:
#             return Response(
#                 {
#                     "detail":
#                     "Email is already verified."
#                 },
#                 status=status.HTTP_200_OK
#             )

#         user.email_verified = True

#         user.save( update_fields=[ "email_verified" ])

#         return Response({"detail":"Email verified successfully."},
#             status=status.HTTP_200_OK
#         )