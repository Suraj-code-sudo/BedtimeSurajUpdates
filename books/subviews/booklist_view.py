from books.models import Book, RecordingRequest
from books.serializers import BookSerializer
from django.db.models import Q, QuerySet
from apps.users.models import CustomUser as User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import (viewsets,)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        #return Book.objects.filter(public=True).prefetch_related("pages")
        return Book.objects.filter(public=True)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        try:
            key = self.request.query_params.get('key')
            RecordingRequest.objects.get(id=key)
            permission_classes = [AllowAny]
        except RecordingRequest.DoesNotExist:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
