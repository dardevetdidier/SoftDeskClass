from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action

from rest_framework.views import APIView

from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-last_name')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
#     @action(detail=True)
#     def users(self, request, pk=None):  # pk != projects/pk/ ?
#         if request.method == 'GET':
#             project = Project.objects.get(pk=pk)
#             print("request: get")
#             users = Contributor.objects.filter(project_id=3)
#             serializer = ContributorSerializer(users, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         if request.method == 'DELETE':
#             user = User.objects.get(pk=pk)
#             user.delete()
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         if request == 'POST':
#             serializer = UserSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response("ok")
#
#     # @action(detail=False, methods=['get'])
#     # def users(self, request):
#     #     serializer = UserSerializer
#     #     users = User.objects.all()
#     #     return Response(users)
#
#     @action(detail=False, methods=['get'])
#     def issues(self, request, project_id, pk=None):
#         if self.request.method == 'GET':
#             print('request: get')
#             queryset = Issue.objects.filter(project_id=project_id)
#             issue = get_object_or_404(queryset, pk=pk)
#             serializer = IssueSerializer(issue)
#             return Response(serializer.data)
#     #
#     @action(detail=True, methods=['delete'])
#     def issues(self, request, pk=None):
#         queryset = Issue.objects.all()
#         issue = get_object_or_404(queryset, pk=pk)
#         issue.delete()
#         return Response(status=status.HTTP_202_ACCEPTED)
#
#
#
#
# class IssueViewSet(viewsets.ModelViewSet):
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#
# class ContributorViewSet(viewsets.ModelViewSet):
#     queryset = Contributor.objects.all()
#     serializer_class = ContributorSerializer

class AuthorAllContributorCreateRead(permissions.BasePermission):

    edit_methods = ('PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print(obj)
        print(request.user)
        print(obj.author_user_id)
        print(obj.contributors.all())

        if obj.author_user_id == request.user:
            return True

        if request.user in obj.contributors.all() and request.method not in self.edit_methods:
            return True

        return False


class ProjectList(APIView):
    """"List of all projects, or create a new project"""
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """Retrieve, update or delete a project instance"""
    permission_classes = [IsAuthenticated, AuthorAllContributorCreateRead, ]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, obj=project)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, obj=project)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, obj=project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorList(APIView):
    """
    List of contributors related to a project, or add a contributor to a project
    """
    def get(self, request, pk):
        contributors = Contributor.objects.filter(project_id=pk)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ContributorDetail(APIView):
    """
    Delete a contributor from a project.
    """
    permission_classes = [IsAuthenticated, AuthorAllContributorCreateRead, ]

    def get_object(self, pk):
        try:
            return Contributor.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def delete(self, request, pk2, *args, **kwargs):
        contributor = self.get_object(pk2)
        self.check_object_permissions(request, obj=contributor)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueList(APIView):
    """
    A list of all Issues related to a project, or create a new issue.
    """
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk=pk)
        self.check_object_permissions(request, obj=project)
        issues = Issue.objects.filter(project_id=project.project_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = IssueSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """
    Retrieve, update or delete an Issue instance.
    """

    def get(self, request, pk, *args, **kwargs):
        pass

    def put(self, request, pk, *args, **kwargs):
        pass

    def delete(self, request, pk, *args, **kwargs):
        pass
