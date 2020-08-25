from rest_framework import serializers
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location

class LocationSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    # slug_name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.slug_name = validated_data.get('slug_name', instance.slug_name)
     

class ProjectCategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return ProjectCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class PledgetypeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    type = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Pledgetype.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    # The source argument (being passed in on the next line) controls which attribute is used to populate a field, and can point at any attribute on the serialized instance, which in this case the attribute is the id and the instance is the instance of a user.
    user = serializers.ReadOnlyField(source='user.id')
    project_id = serializers.IntegerField()
    date_created = serializers.ReadOnlyField()
    type_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get( 'amount', instance.amount) 
        instance.comment = validated_data.get( 'comment', instance.comment) 
        instance.anonymous = validated_data.get( 'anonymous', instance.anonymous) 
        instance.user = validated_data.get( 'user', instance.user) 
        instance.project_id = validated_data.get( 'project_id', instance.project_id) 
        instance.date_created = validated_data.get( 'date_created', instance.date_created) 
        instance.type_id = validated_data.get( 'type_id', instance.type_id) 
        instance.save()
        return instance


#this serializer shows just the project data
class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=800)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')
    due_date = serializers.DateTimeField()
    category_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    
    # this func is required to store the data sent in the POST request to the database..
    def create(self, validated_data):
        # the "**"" unpacks the validated_Data
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.location_id = validated_data.get('location_id', instance.location_id)
        instance.save()
        return instance


# #this serializer inherits from the ProjectSerializer. It shows the project data (everything in the ProjectSerializer) AND all the pledges.
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

