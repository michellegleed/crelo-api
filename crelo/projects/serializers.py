from rest_framework import serializers
from .models import Project, Pledge

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.CharField(max_length=200)
    project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

#this serializer shows just the project data
class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=800)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    creator = serializers.CharField(max_length=200)
    due_date = serializers.DateTimeField()
    
    # this func is required to store the data sent in the POST request to the database..
    def create(self, validated_data):
        # the "**"" unpacks the validated_Data
        return Project.objects.create(**validated_data)

# #this serializer inherits from the ProjectSerializer. It shows the project data (everything in the ProjectSerializer) AND all the pledges.
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

