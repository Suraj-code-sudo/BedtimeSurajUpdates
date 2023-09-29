from books.models import Narration, RecordingRequest, RequestStatus, Recording, RequestStatus
from books.serializers import RecordingSerializer
from django.db.models import Q, QuerySet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import (
    mixins,
    status,
    viewsets,
)

from rest_framework.response import Response
from django.db import transaction
from bedtime.pagination import CustomPagination



class RecordingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer  
        
    def get_queryset(self) -> QuerySet[Recording]:
        user = self.request.user
        book_id = self.request.query_params.get("book", None)
        if book_id:
            narrations = Narration.objects.filter(book=book_id)
            narrations = narrations.filter(Q(public=True) | Q(customized_book__user=user.id))
            recordings = self.queryset.filter(book=book_id, user=user.id)
            combined_data = list(narrations) + list(recordings)
            self.pagination_class = CustomPagination
            return combined_data
        else:
            queryset = self.queryset.filter(user=user.pk).order_by('-book_id').distinct("book_id")
            return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = self.request.user
        recording_request_id = request.data.get('id', None)
        if recording_request_id or request.user.is_anonymous:
            
            try:
                recording_request = RecordingRequest.objects.get(pk=recording_request_id)
                recording_request.status = RequestStatus.FINISHED
                recording_request.save()  
                request.data['narrator_name'] = recording_request.narrator_name        
                user = recording_request.user
            except RecordingRequest.DoesNotExist: 
                return Response(status=status.HTTP_400_BAD_REQUEST)


        recording_name = Recording.objects.filter(
            narrator_name=request.data['narrator_name'], 
            book=request.data['book'],
            user = user
        )
        if recording_name:
            return Response({
                'result':{
                    'message':'Recording with this name already exist for this book!'
                }            
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )

        print(request.data.audio.url)

        serializer.is_valid(raise_exception=True)
        Recording.objects.create(
            user=user, **serializer.validated_data
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
