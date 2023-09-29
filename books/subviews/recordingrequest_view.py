from books.models import RecordingRequest, RequestStatus, Recording, RequestStatus
from books.serializers import RecordingRequestSerializer, AddRecordingRequestSerializer
from django.db.models import Q, QuerySet
from typing import Type, Union
from apps.users.models import CustomUser as User
from rest_framework.permissions import AllowAny, IsAuthenticated
from moviepy.editor import *
from moviepy.audio import *
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

class RecordingRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RecordingRequest.objects.all()
    serializer_class = RecordingRequestSerializer

    def get_queryset(self) -> QuerySet[RecordingRequest]:
        user = self.request.user
        book_id = self.request.query_params.get("book", None)
        queryset = RecordingRequest.objects.all()
        if book_id:
            queryset = queryset.filter(book=book_id)
        if self.action == "retrieve" or self.action == "start":
            return queryset
        return queryset.filter(user=user.pk)

    def get_serializer_class(
        self,
    ) -> Type[Union[RecordingRequestSerializer, AddRecordingRequestSerializer]]:
        if self.action in ("create"):
            return AddRecordingRequestSerializer
        return RecordingRequestSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        assert isinstance(self.request.user, User)
        
        recording_name = Recording.objects.filter(
            narrator_name=request.data['narrator_name'], 
            book=request.data['book'],
            user = self.request.user
        )
        if recording_name:
            return Response({
                'result':{
                    'message':'Recording with this name already exist for this book!',
                }            
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'start':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def start(self, request, pk):
        req = RecordingRequest.objects.get(pk=pk)
        req.status = RequestStatus.STARTED
        req.save()
        
        return Response( status=status.HTTP_200_OK)
