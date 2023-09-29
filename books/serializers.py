from rest_framework import serializers

from .models import Book, Narration, Page, RecordingRequest, Recording, RequestStatus, CombineVideo


class NarrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Narration
        fields = ['audio', 'timestamps', 'book', 'narrator_name', 'public']


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'pages', 'cover', 'thumbnail']


class ChoicesToStringField(serializers.CharField):
    choices_class = None
    name = ""

    def to_representation(self, value) -> str:
        return self.choices_class(value).label

    def to_internal_value(self, value: str):
        try:
            return self.choices_class[value.upper()]
        except KeyError:
            raise serializers.ValidationError(f"Invalid value to represent {self.name}")


class RequestStatusField(ChoicesToStringField):
    choices_class = RequestStatus
    name = "request_status"


class RecordingRequestSerializer(serializers.ModelSerializer):
    status = RequestStatusField()
    requested_url = serializers.SerializerMethodField()

    class Meta:
        model = RecordingRequest
        fields = ['id', 'book', 'narrator_name', 'custom_note', 'requested_url', 'status', 'created_at', 'last_modified']
    
    def get_requested_url(self, obj):
        request = self.context.get("request")
        base_url = f"{request.scheme}://{request.get_host()}"
        return f'{base_url}/request/#/recorder/{obj.book.id}/?key={obj.id}&name={obj.narrator_name}'


class AddRecordingRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecordingRequest
        fields = ['id', 'book', 'narrator_name', 'custom_note']

    def create(self, validated_data):
        request = self.context["request"]
        instance = RecordingRequest.objects.create(
            user=request.user,
            id=request.data["id"],
            **validated_data 
        )
        return instance

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = (
            'user', 'book',
            'narrator_name', 'finalVideo'
        )

class NarrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Narration
        fields = ['audio', 'timestamps', 'book', 'narrator_name', 'public']


class CombineVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombineVideo
        fields = ['book', 'pages', 'audio', 'narrator']