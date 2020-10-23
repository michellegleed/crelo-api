from rest_framework import serializers
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location, ProgressUpdate, Activity
from users.serializers import LimitedUserSerializer

# Importing this to check whether project has passed due date and should be closed.
from django.utils.timezone import now
from datetime import timedelta

# Have to use signals in the serializers just for the milestone serializer method on ProjectSerializer.
from django.dispatch import receiver, Signal

# to calculate current amount pledged on Project serializer
from django.db.models import Avg, Count, Min, Sum

class LocationSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)


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
    comment = serializers.CharField(max_length=800)
    anonymous = serializers.BooleanField()
    # The source argument (being passed in on the next line) controls which attribute is used to populate a field, and can point at any attribute on the serialized instance, which in this case the attribute is the id and the instance is the instance of a user.
    # user = serializers.ReadOnlyField(source='user.id')
    
    user = LimitedUserSerializer(read_only=True)
    project_id = serializers.ReadOnlyField(source='project.id')
    date = serializers.ReadOnlyField()
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
        instance.date = validated_data.get('date', instance.date) 
        instance.type_id = validated_data.get('type_id', instance.type_id) 
        instance.save()
        return instance


class ActivitySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    action = serializers.CharField(max_length=200)
    info = serializers.CharField(max_length=4000)
    date = serializers.ReadOnlyField()
    image = serializers.URLField(required=False)
    user_id = serializers.ReadOnlyField(source='user.id')
    # location = LocationSerializer()
    location_id = serializers.ReadOnlyField(source='location.id')
    project_id = serializers.ReadOnlyField(source='project.id')
    
    def create(self, validated_data):
        return Activity.objects.create(**validated_data)


# class LocationDetailSerializer(serializers.Serializer):
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
    project = serializers.ReadOnlyField(source='project.id')
    date = serializers.ReadOnlyField()
    content = serializers.CharField(max_length=4000)
    image = serializers.URLField(required=False)
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

    activity_data = {
        "action": kwargs.get('action'),
        "info": kwargs.get('info'),
        "image": kwargs.get('image')
        }

    activity_serializer = ActivitySerializer(data=activity_data)
    if activity_serializer.is_valid():
        print("activity serializer is valid!")
        activity_serializer.save(
            user=kwargs.get('user'), 
            project=kwargs.get('project'),
            location=kwargs.get('location')
        )

class LimitedProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    venue = serializers.CharField(max_length=200, default="")
    description = serializers.CharField(max_length=4000)
    pledgetype = serializers.PrimaryKeyRelatedField(queryset=Pledgetype.objects.all())
    goal_amount = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')
    due_date = serializers.DateTimeField()
    # category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    category = ProjectCategorySerializer(read_only=True)
    location = serializers.ReadOnlyField(source='user.location.name')
    last_milestone = serializers.IntegerField(default=0)
    last_chance_triggered = serializers.BooleanField(default=False)
    current_amount_pledged = serializers.ReadOnlyField()
    current_percentage_pledged = serializers.ReadOnlyField()

    def get_check_is_open(self, instance):
            if instance.is_open:
                instance.is_open = instance.due_date > now()
                instance.save()
                return instance


#this serializer shows just the project data
class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    venue = serializers.CharField(max_length=200, default="")
    description = serializers.CharField(max_length=4000)
    pledgetype = serializers.PrimaryKeyRelatedField(queryset=Pledgetype.objects.all())
    goal_amount = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')
    due_date = serializers.DateTimeField()
    category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    # category = ProjectCategorySerializer()
    location = serializers.ReadOnlyField(source='user.location.name')
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

                    activity_signal.send(sender=Project, action="last-chance", info=instance.description, user=instance.user, project=instance, location=location, image=instance.image)

                    instance.last_chance_triggered = True

                    instance.save()
            else:
                if instance.due_date - timedelta(days=5) > now():
                    lastChanceActivityToDelete = Activity.objects.get(action="last-chance", project__id=instance.id)

                    lastChanceActivityToDelete.delete()
                    instance.last_chance_triggered = False
                    instance.save()

    def get_check_for_milestone(self, instance):
        if instance.is_open:
            if instance.last_milestone < 100:
                if instance.current_percentage_pledged > float(instance.last_milestone + 25):
                    instance.last_milestone += 25

                    location = Location.objects.get(pk=instance.location_id)
                    last_milestone = instance.last_milestone
                    user = instance.user
                    project = instance

                    instance.save()

                    activity_signal.send(sender=Project, action="milestone", info=last_milestone, user=user, project=project, location=location, image=project.image)
                while instance.current_percentage_pledged < float(instance.last_milestone):
                    milestoneActivityToDelete = Activity.objects.get(action="milestone", info=instance.last_milestone, project__id=instance.id)

                    milestoneActivityToDelete.delete()
                    instance.last_milestone -= 25
                    instance.save()


                
        
    # this func is required to store the data sent in the POST request to the database..
    def create(self, validated_data):
        # the "**"" unpacks the validated_Data
        return Project.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.description = validated_data.get('description', instance.description)
        instance.goal_amount = validated_data.get('goal_amount', instance.goal_amount)
        # instance.current_amount = validated_data.get('current_amount', instance.current_amount)
        instance.image = validated_data.get('image', instance.image)
        # instance.is_open = validated_data.get('is_open', instance.is_open)
        # instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.category = validated_data.get('category', instance.category)
        # instance.location_id = validated_data.get('location_id', instance.location_id)
        instance.save()
        return instance

    def get_check_is_open(self, instance):
            if instance.is_open:
                instance.is_open = instance.due_date > now()
                instance.save()
                return instance


# #this serializer inherits from the ProjectSerializer. It shows the project data (everything in the ProjectSerializer) AND all the pledges.
class ProjectDetailSerializer(ProjectSerializer):
    updates = ProgressUpdateSerializer(many=True, read_only=True)
    # pledges = PledgeSerializer(many=True, read_only=True)
    project_activity = ActivitySerializer(many=True, read_only=True)

    pledges = serializers.SerializerMethodField()

    user = LimitedUserSerializer(read_only=True)

    def get_pledges(self, instance):
         ordered_queryset = instance.pledges.all().order_by('-amount','-date')
         return PledgeSerializer(ordered_queryset, many=True, context=self.context).data

    # increment_project_views = serializers.SerializerMethodField()

    # the view checks to make sure the logged in user is not the project creator before running this increment_project_views()    
    # def get_increment_project_views(self, instance):
    #     instance.project_views = instance.project_views + 1
    #     instance.save()
        


class ProjectAnalyticsSerializer(ProjectDetailSerializer):
    view_count = serializers.IntegerField()
    pledge_count = serializers.SerializerMethodField()
    conversion_rate = serializers.SerializerMethodField()
    average_pledge = serializers.SerializerMethodField()

    def get_pledge_count(self, instance):
        if instance.current_amount_pledged != None:
            return instance.pledges.count()

    def get_average_pledge(self, instance):
        if instance.current_amount_pledged != None:
            # instance.average_pledge = instance.current_amount_pledged / len(instance.pledges)
            # instance.save()
            return round(instance.current_amount_pledged / instance.pledges.count(), 2)
        return 0
            
    def get_conversion_rate(self, instance):
        if instance.current_amount_pledged != None:
            # instance.average_pledge = instance.current_amount_pledged / len(instance.pledges)
            # instance.save()
            return round((instance.pledge_count / instance.view_count) * 100, 1)
        return 0
    


class ActivityDetailSerializer(ActivitySerializer):
    project = LimitedProjectSerializer(read_only=True)


class LocationDetailSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    # slug_name = serializers.CharField(max_length=50)

    activity = serializers.SerializerMethodField()

    def get_activity(self, instance):
        # We are doing this because we only want to get the activity for open projects!!
        ordered_queryset = instance.location_activity.all().order_by('-date')
        open_project_activities = [item for item in ordered_queryset if item.project.is_open]
        final_activity_feed = open_project_activities[:18]

        return ActivityDetailSerializer(final_activity_feed, many=True, context=self.context).data
        
        # this returns the activity of both open and closed projects...
        # return ActivityDetailSerializer(ordered_queryset, many=True, context=self.context).data

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.slug_name = validated_data.get('slug_name', instance.slug_name)
        instance.save()
        return instance

class ExtendedPledgeSerializer(PledgeSerializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=800)
    anonymous = serializers.BooleanField()
    # The source argument (being passed in on the next line) controls which attribute is used to populate a field, and can point at any attribute on the serialized instance, which in this case the attribute is the id and the instance is the instance of a user.
    # user = serializers.ReadOnlyField(source='user.id')
    
    user = LimitedUserSerializer(read_only=True)
    # project_id = serializers.ReadOnlyField(source='project.id')
    project = ProjectSerializer(read_only=True)
    date = serializers.ReadOnlyField()
    type_id = serializers.ReadOnlyField(source='project.pledgetype.id')