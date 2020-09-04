from rest_framework import serializers
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location, ProgressUpdate, Activity

# Importing this to check whether project has passed due date and should be closed.
from django.utils.timezone import now
from datetime import timedelta

# Have to use signals in the serializers just for the milestone serializer method on ProjectSerializer.
from django.dispatch import receiver, Signal

# to calculate current amount pledged on Project serializer
from django.db.models import Avg, Count, Min, Sum


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
    project_id = serializers.ReadOnlyField(source='project.id')
    date_created = serializers.ReadOnlyField()
    # type_id = serializers.IntegerField()
    type_id = serializers.ReadOnlyField(source='project.pledgetype.id')

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount) 
        instance.comment = validated_data.get('comment', instance.comment) 
        instance.anonymous = validated_data.get('anonymous', instance.anonymous) 
        instance.user = validated_data.get('user', instance.user) 
        instance.project_id = validated_data.get('project_id', instance.project_id) 
        instance.date_created = validated_data.get('date_created', instance.date_created) 
        instance.type_id = validated_data.get('type_id', instance.type_id) 
        instance.save()
        return instance


class ActivitySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    action = serializers.CharField(max_length=200)
    datetime = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField(source='user.id')
    location_id = serializers.ReadOnlyField(source='location.id')
    project_id = serializers.ReadOnlyField(source='project.id')
    
    def create(self, validated_data):
        return Activity.objects.create(**validated_data)


# class LocationSerializer(serializers.Serializer):
#     id = serializers.ReadOnlyField()
#     name = serializers.CharField(max_length=200)
#     # slug_name = serializers.CharField(max_length=50)

#     activity = serializers.SerializerMethodField()

#     def get_activity(self, instance):
#          ordered_queryset = instance.location_activity.all().order_by('-datetime')
#          return ActivitySerializer(ordered_queryset, many=True, context=self.context).data

#     def create(self, validated_data):
#         return Location.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         # instance.slug_name = validated_data.get('slug_name', instance.slug_name)
#         instance.save()
#         return instance

     

class ProgressUpdateSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    project_id = serializers.ReadOnlyField(source='project.id')
    date_posted = serializers.ReadOnlyField()
    content = serializers.CharField(max_length=2000)
    user = serializers.ReadOnlyField(source='project.user.id')

    def create(self, validated_data):
        return ProgressUpdate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content) 
        instance.save()
        return instance

# SIGNAL FUNCTIONS...

activity_signal = Signal(providing_args=['action'])

@receiver(activity_signal)
def activity_signal_receiver(sender, **kwargs):
    print("activity signal was triggered. kwargs = ", kwargs)

    activity_data = {"action": kwargs.get('action')}

    activity_serializer = ActivitySerializer(data=activity_data)
    if activity_serializer.is_valid():
        print("activity serialize is valid!")
        activity_serializer.save(
            user=kwargs.get('user'), 
            project=kwargs.get('project'),
            location=kwargs.get('location')
        )

#this serializer shows just the project data
class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    venue = serializers.CharField(max_length=200, default="")
    description = serializers.CharField(max_length=800)
    pledgetype = serializers.PrimaryKeyRelatedField(queryset=Pledgetype.objects.all())
    goal_amount = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')
    due_date = serializers.DateTimeField()
    category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    location_id = serializers.ReadOnlyField(source='user.location.id')
    last_milestone = serializers.IntegerField(default=0)
    last_chance_triggered = serializers.BooleanField(default=False)
    current_amount_pledged = serializers.ReadOnlyField()
    current_percentage_pledged = serializers.ReadOnlyField()

    check_for_milestone = serializers.SerializerMethodField()
    check_close_to_due_date = serializers.SerializerMethodField()

    def get_check_close_to_due_date(self, instance):
        if instance.is_open:
            if instance.last_chance_triggered == False:
                if instance.due_date - timedelta(days=5) < now():
                    location = Location.objects.get(pk=instance.location_id)

                    activity_signal.send(sender=Project, action="last-chance", user=instance.user, project=instance, location=location)

                    instance.last_chance_triggered = True

                    instance.save()

    def get_check_for_milestone(self, instance):
        if instance.is_open:
            if instance.current_percentage_pledged > float(instance.last_milestone + 25):
                instance.last_milestone += 25

                location = Location.objects.get(pk=instance.location_id)

                activity_signal.send(sender=Project, action="milestone", user=instance.user, project=instance, location=location)

                instance.save()
        
    # this func is required to store the data sent in the POST request to the database..
    def create(self, validated_data):
        # the "**"" unpacks the validated_Data
        print("the validated data looks like this: ", validated_data)
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal_amount = validated_data.get('goal_amount', instance.goal_amount)
        # instance.current_amount = validated_data.get('current_amount', instance.current_amount)
        instance.image = validated_data.get('image', instance.image)
        # instance.is_open = validated_data.get('is_open', instance.is_open)
        # instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        # instance.location_id = validated_data.get('location_id', instance.location_id)
        instance.save()
        return instance


# #this serializer inherits from the ProjectSerializer. It shows the project data (everything in the ProjectSerializer) AND all the pledges.
class ProjectDetailSerializer(ProjectSerializer):
    updates = ProgressUpdateSerializer(many=True, read_only=True)
    # pledges = PledgeSerializer(many=True, read_only=True)
    project_activity = ActivitySerializer(many=True, read_only=True)

    pledges = serializers.SerializerMethodField()

    def get_pledges(self, instance):
         ordered_queryset = instance.pledges.all().order_by('-amount','-date_created')
         return PledgeSerializer(ordered_queryset, many=True, context=self.context).data


class ActivityDetailSerializer(ActivitySerializer):
    project = ProjectSerializer(read_only=True)


class LocationSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    # slug_name = serializers.CharField(max_length=50)

    activity = serializers.SerializerMethodField()

    def get_activity(self, instance):
         ordered_queryset = instance.location_activity.all().order_by('-datetime')
         return ActivityDetailSerializer(ordered_queryset, many=True, context=self.context).data

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.slug_name = validated_data.get('slug_name', instance.slug_name)
        instance.save()
        return instance