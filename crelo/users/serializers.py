from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    location_id = serializers.IntegerField()

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
        instance.username = validated_data.get('username', instance.username)
        instance.location_id = validated_data.get('location_id', instance.location_id)

        instance.save()

        return instance
      
        
       