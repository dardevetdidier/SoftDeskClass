from django.contrib.auth.models import User
from rest_framework import serializers


from .models import Project, Contributor, Comment, Issue, TYPE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    contributors = UserSerializer(many=True, read_only=True)
    issues = IssueSerializer(many=True, read_only=True)
    type = serializers.ChoiceField(TYPE_CHOICES)

    class Meta:
        model = Project
        fields = "__all__"







