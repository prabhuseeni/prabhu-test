import jwt
from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User#Register API

from django.http import HttpResponse

from rest_framework import viewsets, pagination, status,mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class QueryViewSet(viewsets.ModelViewSet):
    # authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    queryset = Query.objects.all()  # .order_by('name')
    serializer_class = QuerySerializer

    def create(self, request, *args, **kwargs):

        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # here chacking event start and end date

        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            return super().update(request, *args, **kwargs)


    def get_queryset(self):
        pagination.PageNumberPagination.page_size = self.request.query_params.get('page_size', 10)
        queryset = Query.objects.all().order_by('-creation_timestamp')
        try:
            filterBy_query_uuid = self.request.query_params.get('query_uuid', None)

            filterBy_pk = self.kwargs.get('pk')
            if filterBy_query_uuid is not None:

                try:
                    queryset = queryset.filter(query_uuid=filterBy_query_uuid)
                except Exception as e:
                    print("Error: query_uuid '{}' not found".format(filterBy_query_uuid))
                    return queryset.objects.none()
            elif filterBy_pk:
                try:
                    return queryset.filter(pk=filterBy_pk)
                except Exception as e:
                    print("Error: pk '{}' not found".format(filterBy_query_uuid))
                    return queryset.objects.none()

            else:
                return queryset

        except Exception as e:
            print(e)
            return Query.objects.none()
