from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Pledgetype, ProjectCategory, Location
from .serializers import ProjectSerializer, ProjectDetailSerializer, PledgeSerializer, PledgetypeSerializer, ProjectCategorySerializer, LocationSerializer

# TODO: Have to add PUT and DELETE to  these views!


class ProjectList(APIView):

    def get(self, request):
        projects = Project.objects.all()
        # note, in the serializer we have to pass in many=True. What it means in DRF is since your serializer.data is going to be a list and each item in the list needs to be converted to json. So it's many because there's more than one object to be parsed.
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProjectDetail(APIView):

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    #CREATOR ONLY!!! Might need to use a mixin??
    def put(self, request, pk):
        project = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = ProjectDetailSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PledgeList(APIView):

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
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


class PledgeDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
        serializer = PledgeSerializer(pledge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # status=200 so no need to include - it's the default.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pledge = self.get_object(pk)
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
    
    #ADMIN ONLY!!! Might need to use a mixin??
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
    
    #ADMIN ONLY!!! Might need to use a mixin??
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LocationList(APIView):

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