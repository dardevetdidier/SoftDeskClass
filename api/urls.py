from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name="projects"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
    path('projects/<int:pk>/users/', views.ContributorList.as_view(), name='project-contributors'),
    path('projects/<int:pk>/users/<int:pk2>/', views.ContributorDetail.as_view(), name='project-contributors-detail'),
    path('projects/<int:pk>/issues/', views.IssueList.as_view(), name='project-issues'),
    # path('projects/<int:pk>/issues/<int:pk2>/', views.issue_detail, name='project_issue-detail'),
    # path('projects/<int:pk>/issues/<int:pk2>/comments/', views.comment_list, name='issue-comments'),
    # path('projects/<int:pk>/issues/<int:pk2>/comments/<int:pk3>/', views.comment_detail, name='issue-comment-detail'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
