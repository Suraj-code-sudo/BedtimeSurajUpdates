from books.models import Narration
from books.serializers import NarrationSerializer
from django.db.models import Q, QuerySet

from rest_framework import (viewsets)


class NarrationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer

    def get_queryset(self) -> QuerySet[Narration]:
        user = self.request.user
        book_id = self.request.query_params.get("book", None)
        queryset = Narration.objects.all()
        if book_id:
            queryset = queryset.filter(book=book_id)
        return queryset.filter(Q(public=True) | Q(customized_book__user=user.pk))
