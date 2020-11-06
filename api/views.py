from django.contrib.auth.models import User

from .models import Score
from rest_framework import viewsets, filters
from rest_framework import permissions
from .serializers import UserSerializer, ScoreSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = User.objects.all()
        return user


class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        score = Score.objects.filter(user=self.request.user).order_by('-id')
        return score

    # very important!
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BestScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']

    def get_queryset(self):
        best = Score.objects.filter(user=self.request.user)
        return best

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('name')[:1])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WorstScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']

    def get_queryset(self):
        worst = Score.objects.filter(user=self.request.user)
        return worst

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-name')[:1])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

