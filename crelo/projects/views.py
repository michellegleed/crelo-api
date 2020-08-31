from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location, ProgressUpdate, Activity
from .serializers import ProjectSerializer, ProjectDetailSerializer, PledgeSerializer, PledgetypeSerializer, ProjectCategorySerializer, LocationSerializer, ProgressUpdateSerializer, ActivitySerializer

from django.dispatch import receiver, Signal

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

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

    # def post(self, request):
    #     serializer = PledgetypeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # activity_data = {"action": "new-project", "object_model": "Project", "object_id": serializer.data['id']}
            
    #         if activity_serializer.is_valid():
    #             project = Project.objects.get(pk=serializer.data['id'])
    #             activity_serializer.save(
    #                 user=request.user, 
    #                 project=project,
    #                 location=request.user.location
    #             )


class ProjectList(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        # note, in the serializer we have to pass in many=True. What it means in DRF is since your serializer.data is going to be a list and each item in the list needs to be converted to json. So it's many because there's more than one object to be parsed.
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            print("about to save the new project serializer")
            serializer.save(user=request.user, location_id=request.user.location.id)

            project = Project.objects.get(pk=serializer.data['id'])

            activity_signal.send(sender=ProgressUpdate, action="project-created", user=request.user, project=project, location=request.user.location)

            # activity_data = {"action": "new-project", "object_model": "Project", "object_id": serializer.data['id']}
            # activity_serializer = ActivitySerializer(data=activity_data)
            # if activity_serializer.is_valid():
            #     project = Project.objects.get(pk=serializer.data['id'])
            #     activity_serializer.save(
            #         user=request.user, 
            #         project=project,
            #         location=request.user.location
            #     )
            #     return Response(
            #         serializer.data,
            #         status=status.HTTP_201_CREATED
            #         )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class ProjectDetail(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = ProjectDetailSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgressUpdateList(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, project_pk):
        progress_updates = ProgressUpdate.objects.filter(project_id=project_pk)
        serializer = ProgressUpdateSerializer(progress_updates, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk):

        serializer = ProgressUpdateSerializer(data=request.data)

        project = Project.objects.get(pk=project_pk)
        location = Location.objects.get(pk=project.location_id)

        if serializer.is_valid():
            serializer.save(project_id=project)

            activity_signal.send(sender=ProgressUpdate, action="progress-update", user=request.user, project=project, location=location)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        

class ProgressUpdateDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, update_pk):
        try:
            return Project.objects.get(pk=update_pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, update_pk):
        progress_update = self.get_object(update_pk)
        serializer = ProgressUpdateSerializer(progress_update)
        return Response(serializer.data)

    def put(self, request, update_pk):
        progress_update = self.get_object(update_pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = ProgressUpdateSerializer(progress_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, update_pk):
        progress_update = self.get_object(update_pk)
        progress_update.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PledgeList(APIView):

    def get(self, request, project_pk):
        pledges = Pledge.objects.filter(project_id=project_pk)
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = PledgeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    def post(self, request, project_pk):
        pledge_serializer = PledgeSerializer(data=request.data)
        if pledge_serializer.is_valid():
            project = Project.objects.get(id=project_pk)
            amt = project.current_amount + request.data['amount']
            project_serializer = ProjectSerializer(project, {"current_amount": amt}, partial=True)

            pledge_serializer.save(user=request.user, project_id=project_pk, type_id=project.pledgetype.id)

            if project_serializer.is_valid():
                project_serializer.save()
            
                return Response(
                    pledge_serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            pledge_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PledgeDetail(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, project_pk, pledge_pk):
        pledge = self.get_object(pledge_pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     pledge = self.get_object(pk)
    #     # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
    #     serializer = PledgeSerializer(pledge, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data) # status=200 so no need to include - it's the default.
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     pledge = self.get_object(pk)
    #     pledge.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, project_pk, pledge_pk):
        pledge = self.get_object(pledge_pk)
        project = Project.objects.get(id=project_pk)
        amt = project.current_amount - pledge.amount
        project_serializer = ProjectSerializer(project, {"current_amount": amt}, partial=True)
        
        if project_serializer.is_valid():
            project_serializer.save()
            pledge.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PledgetypeList(APIView):

    def get(self, request):
        pledgetypes = Pledgetype.objects.all()
        serializer = PledgetypeSerializer(pledgetypes, many=True)
        return Response(serializer.data)

    #ADMIN ONLY!!! Might need to use a mixin??
    def post(self, request):
        serializer = PledgetypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PledgetypeDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Pledgetype.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledgetype = self.get_object(pk)
        serializer = PledgetypeSerializer(pledgetype)
        return Response(serializer.data)
    
    #ADMIN ONLY!!! 
    def put(self, request, pk):
        pledgetype = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = PledgetypeSerializer(pledgetype, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pledgetype = self.get_object(pk)
        pledgetype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCategoryList(APIView):

    def get(self, request):
        categories = ProjectCategory.objects.all()
        serializer = ProjectCategorySerializer(categories, many=True)
        return Response(serializer.data)

    #ADMIN ONLY!!! Might need to use a mixin??
    def post(self, request):
        serializer = ProjectCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProjectCategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return ProjectCategory.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = ProjectCategorySerializer(category)
        return Response(serializer.data)
    
    #ADMIN ONLY!!!
    def put(self, request, pk):
        category = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = ProjectCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationList(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)

    #ADMIN ONLY!!! Might need to use a mixin??
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

        # def get_object(self):
        #     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        #     self.check_object_permissions(self.request, obj)
        #     return obj


class LocationDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)
    
    #ADMIN ONLY!!! Might need to use a mixin??
    def put(self, request, pk):
        location = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class LocationSLUGDetail(APIView):

#     def get(self, request, location):
#         location = Location.objects.get(slug_name=location)
#         serializer = LocationSerializer(location)
#         return Response(serializer.data)


class ProjectListByLocation(APIView):

    def get(self, request, pk):
        projects = Project.objects.filter(location=pk, is_open=True)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectListByLocationAndCategory(APIView):

    def get(self, request, loc_pk, cat_pk):
        projects = Project.objects.filter(location=loc_pk, category=cat_pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectListFiltered(APIView):

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        user_categories = ProjectCategory.objects.filter(customuser__id=self.request.user.id)

        projects = Project.objects.none()

         # adding the query sets together using the "|" 
        for cat_id in user_categories:
            projects = projects |Project.objects.filter(category=cat_id)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


# class LocationSLUGDetail(APIView):

#     def get(self, request, location):
#         location = Location.objects.get(slug_name=location)
#         serializer = LocationSerializer(location)
#         return Response(serializer.data)


class AllActivity(APIView):

    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

class LocationActivity(APIView):
    def get(self, request, pk):
        
        activity_feed = Activity.objects.filter(location=pk).order_by('-datetime')

        serializer = ActivitySerializer(activity_feed, many=True)

        return Response(serializer.data)

        # activity_data = []
        # for item in activity_feed:

        #     if item.action == "progress-update":
        #         dict = { "action": item.action }
        #         progress_update = ProgressUpdate.objects.get(pk=item.object_id)
        #         serializer = ProgressUpdateSerializer(progress_update)

        #         for key in serializer.data:
        #             dict[str(key)] = serializer.data[str(key)]

        #         project = Project.objects.get(pk=item.project_id)
        #         project_serializer = ProjectSerializer(project)
        #         dict["project"] = project_serializer.data
                
        #         activity_data.append(dict)

        #     if item.action == "new-project":
        #         dict = { "action": item.action }
        #         project = Project.objects.get(pk=item.object_id)
        #         serializer = ProjectSerializer(project)

        #         for key in serializer.data:
        #             dict[str(key)] = serializer.data[str(key)]

        #         activity_data.append(dict)

        #     if item.action == "milestone":
        #         dict = { "action": item.action }
        #         project = Project.objects.get(pk=item.object_id)
        #         serializer = ProjectSerializer(project)

        #         for key in serializer.data:
        #             dict[str(key)] = serializer.data[str(key)]

        #         activity_data.append(dict)

        # return Response(activity_data)

