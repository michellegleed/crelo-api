from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location, ProgressUpdate
from .serializers import ProjectSerializer, ProjectDetailSerializer, PledgeSerializer, PledgetypeSerializer, ProjectCategorySerializer, LocationSerializer, ProgressUpdateSerializer

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


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
            serializer.save(user=request.user)
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get(self, request, project_pk):
        progress_updates = ProgressUpdate.objects.get(project__id=project_pk)
        serializer = ProgressUpdateSerializer(progress_updates, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk):
        pass

        # UP TO HERE!! :)

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

            pledge_serializer.save(user=request.user, project_id=project_pk)
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
        projects = Project.objects.filter(location=pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectListByLocationAndCategory(APIView):

    def get(self, request, loc_pk, cat_pk):
        projects = Project.objects.filter(location=loc_pk, category=cat_pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)