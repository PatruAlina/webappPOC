from django.contrib.auth.models import User
from rest_framework import serializers

from pentagram.models import Photo,Comment,Likes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password','email')

    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Photo
        fields=('id','user','photo')
    def create(self,validated_data):
        photo=Photo.objects.create(**validated_data)
        photo.save()
        return photo

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','user','comment','photo')
    def create(self,validated_data):
        comment=Comment.objects.create(**validated_data)
        comment.save()
        return comment
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields=('id','user','photo')
    def create(self,validated_data):
        likes=Likes.objects.create(**validated_data)
        likes.save()
        return likes