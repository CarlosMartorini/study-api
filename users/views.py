from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UsersSerializer
from rest_framework import status
from django.db.utils import IntegrityError


class Create(APIView):
    def post(self, request):
        data = request.data

        try:
            username = data['username']
            password = data['password']
            is_staff = data['is_staff']
            is_superuser = data['is_superuser']

            new_user = User.object.create_user(
                username=username,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            serialized = UsersSerializer(new_user)
            
            return Response(serialized, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({'error': 'User already exists!'}, status=status.HTTP_409_CONFLICT)


class Login(APIView):
    def post(self, request):
        data = request.data
        try:
            username = data['username']
            password = data['password']

            logged_user = authenticate(
                username=username,
                password=password
            )

            if logged_user:
                token = Token.objects.get_or_created(user=logged_user)[0]
                return Response({'token': token.key})
            
            return Response({'error': 'Username or password may be wrong!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except KeyError:
            return Response({'error': f"{str(KeyError)} it's missing"}, status=status.HTTP_406_NOT_ACCEPTABLE)

