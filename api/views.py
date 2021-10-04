from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from .permissions import ProjectAuthorAllContributorCreateRead, IssueAuthorAllContributorCreateRead, CommentAuthorAllContributorCreateRead
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor


class ProjectList(APIView):
    """"List of all projects, or create a new project"""
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        projects = Project.objects.filter(contributors__exact=self.request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.validated_data["author_user_id"] = request.user
            serializer.save()
            contributor = Contributor(user_id=request.user,
                                      project_id=Project.objects.last(),
                                      permission="CRUD",
                                      role="auteur")
            contributor.save()
            ContributorSerializer(contributor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """Retrieve, update or delete a project instance"""
    permission_classes = [IsAuthenticated, ProjectAuthorAllContributorCreateRead]

    @staticmethod
    def get_object(pk):
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
        project = Project.objects.get(pk=pk)
        contributors = Contributor.objects.filter(project_id=pk)
        if self.request.user in project.contributors.all():
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()

    def post(self, request, pk, *args, **kwargs):
        project = Project.objects.get(pk=pk)
        if self.request.user == project.author_user_id:
            serializer = ContributorSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied


class ContributorDetail(APIView):
    """
    Delete a contributor from a project.
    """
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get_object(pk):
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

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        issues = Issue.objects.filter(project_id=project.pk)
        if self.request.user in project.contributors.all():
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()

    def post(self, request, pk, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.contributors.all():
            serializer = IssueSerializer(data=self.request.data)

            if serializer.is_valid():
                serializer.validated_data["assignee_user_id"] = self.request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied()


class IssueDetail(APIView):
    """
    Retrieve, update or delete an Issue instance.
    """
    permission_classes = [IsAuthenticated, IssueAuthorAllContributorCreateRead]

    @staticmethod
    def get_object(pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, pk2, *args, **kwargs):
        issue = self.get_object(pk=pk2)
        self.check_object_permissions(request, obj=issue)
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk2, *args, **kwargs):
        issue = self.get_object(pk2)
        serializer = IssueSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk2, *args, **kwargs):
        issue = self.get_object(pk2)
        self.check_object_permissions(request, obj=issue)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """List of all comments related to an issue, or create a new comment."""

    def get(self, request, pk, pk2, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        issue = get_object_or_404(Issue, pk=pk2)
        comments = Comment.objects.filter(issue_id=issue)
        if self.request.user in project.contributors.all():
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()

    def post(self, request, pk, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.contributors.all():
            serializer = CommentSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied()


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment.
    """
    permission_classes = [IsAuthenticated, CommentAuthorAllContributorCreateRead]

    @staticmethod
    def get_object(pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk3, *args, **kwargs):
        comment = self.get_object(pk=pk3)
        self.check_object_permissions(request, obj=comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk3, *args, **kwargs):
        comment = self.get_object(pk=pk3)
        self.check_object_permissions(request, obj=comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk3, *args, **kwargs):
        comment = self.get_object(pk=pk3)
        self.check_object_permissions(request, obj=comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
