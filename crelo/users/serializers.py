from rest_framework import serializers
from .models import CustomUser

from projects.models import ProjectCategory

class CustomUserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    location_id = serializers.IntegerField()
    bio = serializers.CharField(max_length=2000, required=False)
    image = serializers.URLField(required=False)
    favourite_categories = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all(), many=True, required=False)

    def create(self, validated_data):

        new_user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            location_id=validated_data['location_id']
        )
        new_user.set_password(validated_data['password'])

        new_user.save()

        return new_user

    def update(self, instance, validated_data):

        print("validated data: ", validated_data)

        instance.username = validated_data.get('username', instance.username)
        instance.location_id = validated_data.get('location_id', instance.location_id)
        if validated_data.get('bio'):
            instance.bio = validated_data['bio']
        if validated_data.get('image'):
            instance.image = validated_data['image']

        if 'favourite_categories' in validated_data:
            cats = validated_data['favourite_categories']
            instance.favourite_categories.set(cats)

        instance.save()

        return instance
      
# For the "created by" section on the project detail pages and the "pledged by" section of the pledge cards...
class LimitedUserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    image = serializers.URLField(required=False)


      