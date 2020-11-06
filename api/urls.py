from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ScoreViewSet, BestScoreViewSet, \
    WorstScoreViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('scores', ScoreViewSet, basename='score')
router.register('best', BestScoreViewSet, basename='best')
router.register('worst', WorstScoreViewSet, basename='worst')

urlpatterns = [
    path('', include(router.urls)),
]
