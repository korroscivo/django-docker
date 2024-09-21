from urllib import request
from venv import create
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import UserSerializer
from .models import CustomUser


from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    if not "email" in request.data:
        return Response({"error": "No email in data"}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(CustomUser, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, create = Token.objects.get_or_create(user=user)
    
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user = CustomUser.objects.get(email=serializer.data['email'])
        user.set_password(request.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        
        return Response({'token':token.key, 'user':serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    UserSerializer(data=request.data)
    
    
    print(request.query_params)
    print(request.tenant)
    return Response({})