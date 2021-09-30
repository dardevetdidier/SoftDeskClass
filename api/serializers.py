from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Project, Contributor, Comment, Issue, TYPE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class ContributorSerializer(serializers.ModelSerializer):
    # user_id = serializers.PrimaryKeyRelatedField(validators=[UniqueValidator(queryset=User.objects.all())],
    #                                              read_only=True)
    # project_id = serializers.PrimaryKeyRelatedField
    class Meta:
        model = Contributor
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # author_user_id = serializers.StringRelatedField()

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







