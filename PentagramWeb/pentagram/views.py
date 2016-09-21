from itertools import count

from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseBadRequest
from rest_framework import status
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
import json
import requests
from django.shortcuts import redirect
from rest_framework.decorators import api_view,permission_classes

from pentagram.models import Photo,Comment,Likes
from pentagram.serializers import UserSerializer,PhotoSerializer,CommentSerializer,LikesSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.
def login_auth(request,template_name):
    if request.method=='POST':
        username= request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            url=''.join(['http://',get_current_site(request).domain,reverse('fetch_token')])
            response=requests.post(url, json={"username":username,"password":password})
            return HttpResponse(response.text,content_type='application/json',status=status.HTTP_200_OK)
        else:
            return HttpResponseBadRequest()
    else:
        if isinstance(request.user,User):
            return redirect(reverse('homepage'))
        context={}
        return TemplateResponse(request,template_name,context)

@api_view(['POST'])
@permission_classes((AllowAny,))
def users(request):
    if request.method =='POST':
        user_serializer=UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=user_serializer.errors)
@api_view(['GET','POST'])
@permission_classes((AllowAny,))
def photos(request):
    if request.method=='GET':
        photos=Photo.objects.all()
        serializer=PhotoSerializer(photos,many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    if request.method =='POST':
        photo_serializer=PhotoSerializer(data=request.data)
        if photo_serializer.is_valid():
            photo_serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=photo_serializer.errors)


@api_view(['GET'])
@permission_classes((AllowAny,))
def photo_id(request,id_photo):
    if request.method=='GET':
        photo=Photo.objects.get(id=id_photo)
        if photo is not None:
            serializer=PhotoSerializer(photo)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes((AllowAny,))
def comments(request,id_photo):
    if request.method=='GET':
        comments=Comment.objects.filter(photo=id_photo)
        serializer=CommentSerializer(comments,many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    if request.method =='POST':
        data = request.data
        data['photo']=id_photo
        comment_serializer=CommentSerializer(data=data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=comment_serializer.errors)

@api_view(['GET','POST','DELETE'])
@permission_classes((AllowAny,))
def likes(request,id_photo):
    if request.method=='GET':
        counted=Likes.objects.filter(photo=id_photo).count()
        return Response(status=status.HTTP_200_OK, data=counted)
    if request.method =='POST':
        data = request.data
        data['photo']=id_photo
        data['user']=request.user.id
        like_serializer=LikesSerializer(data=data)
        if like_serializer.is_valid():
            like_serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=like_serializer.errors)
    if request.method=='DELETE':
        try:
            Likes.objects.filter(photo=id_photo,user=request.user.id).delete()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)
        return Response(status=status.HTTP_200_OK)
