from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('reviews', ReviewViewSet)
router.register('skills', SkillViewSet)
router.register('tags', TagViewSet)
router.register('messages', MessageViewSet)
router.register('project_viewset', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('project_function/', get_projects),
    path('project_apiview/', ProjectAPIView.as_view()),
    path('project_mixin/', ProjectMixin.as_view()),
    path('project_generic/', ProjectGeneric.as_view()),
    # path('project_viewset/', ProjectViewSet),
    path('project/<int:pk>/vote/', set_project_vote)
]
