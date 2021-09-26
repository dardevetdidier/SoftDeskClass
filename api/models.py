from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

TYPE_CHOICES = [('back-end', 'back-end'), ('front-end', 'front-end'), ('IOS', 'IOS'), ('android', 'android')]
TAG_CHOICES = [('bug', 'bug'), ('tâche', 'tâche'), ('amélioration', 'amélioration')]
PRIORITY_CHOICES = [('faible', 'faible'), ('moyenne', 'moyenne'), ('élevée', 'élevée')]
STATUS_CHOICES = [('à faire', 'à faire'), ('en cours', 'en cours'), ('terminé', 'terminé')]
PERMISSION_CHOICES = [('CRUD', 'CRUD'), ('CR', 'CR')]


class Project(models.Model):
    project_id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField('Project title', max_length=100)
    description = models.CharField('Project description', max_length=200)
    type = models.CharField('Project Type', max_length=50, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(to=User,
                                       default=None,
                                       on_delete=models.CASCADE,
                                       )
    contributors = models.ManyToManyField(to=User,
                                          through='Contributor',
                                          blank=True,
                                          related_name='contributors')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE, blank=True)
    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user_id}"


class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=User,
                                       on_delete=models.CASCADE,
                                       related_name='author_user_id')
    assignee_user_id = models.ForeignKey(to=User,
                                         default=author_user_id,
                                         on_delete=models.CASCADE,
                                         related_name='assignee_user_id')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue id: {self.pk}"


class Comment(models.Model):
    comment_id = models.AutoField(auto_created=True, primary_key=True)
    description = models.CharField(max_length=200)
    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment id : {self.comment_id} - description : {self.description}"
