import uuid
from books.models import Book
from books.serializers import BookSerializer

from rest_framework import (
    status,
    viewsets,
)
from rest_framework.response import Response



class UrlViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request):
        base_url = f"{request.scheme}://{request.get_host()}"
        book_id = request.query_params.get('book')
        generated_uuid = uuid.uuid4()
        try:
            book = self.get_queryset().get(id=book_id)
            url = f'{base_url}/request/#/recorder/{book.id}/?key={generated_uuid}'
            return Response(
                {"url": url},
                status=status.HTTP_200_OK
            )
        except Book.DoesNotExist:
            return Response(
                {"error": "Book does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
