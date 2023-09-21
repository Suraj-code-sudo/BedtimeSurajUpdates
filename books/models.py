from django.db import models
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def upload_location(instance, filename):
    extension = "mp3"
    unique_id = f"self_recordings/{uuid.uuid4()}"
    return '%s.%s' % (unique_id, extension)

def upload_video(instance, filename):
    extension = "mp4"
    unique_id = f"combined_video/{uuid.uuid4()}"
    return '%s.%s' % (unique_id, extension)


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    # We sometimes don't want the books to show up.
    public = models.BooleanField(default=True)

    # Cover image will be high resolution and represent the book.
    cover = models.ImageField(null=True, blank=True)

    # Thumnail will be a smaller version of the cover.
    thumbnail = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="pages")
    page_number = models.PositiveIntegerField()
    label = models.CharField(max_length=10)
    image = models.FileField(upload_to=upload_video)

    class Meta:
        ordering = ["book", "page_number"]

    def __str__(self):
        return f"book: {self.book.id} - {self.label}"


class CustomizedBook(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customized_books")


class Narration(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="narrations")

    narrator_name = models.CharField(max_length=200)
    timestamps = models.JSONField()
    audio = models.FileField(upload_to=upload_location)

    # The narration is either public or linked to a specific customized_book belonging to a certain user.
    public = models.BooleanField(default=False)
    customized_book = models.ForeignKey(
        "CustomizedBook", null=True, blank=True, on_delete=models.CASCADE, related_name="narrations"
    )

    class Meta:
        ordering = ["book", "pk"]


class RequestStatus(models.IntegerChoices):
    NEW = 1, _("New")
    STARTED = 2, _("Started")
    FINISHED = 3, _("Finished")


class RecordingRequest(models.Model):
    # Use UUID for id so we can generate a unique link for each request that is not guessable.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recording_requests")
    # Currently we always expect the book to be set, but it could also be some different type of content.
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="recording_requests", null=True, blank=True)

    narrator_name = models.CharField(max_length=200)
    custom_note = models.TextField()

    status = models.IntegerField(choices=RequestStatus.choices, default=RequestStatus.NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # TODO: add expiration date (e.g. only valid for 2 weeks)

    class Meta:
        ordering = ["user", "-created_at"]


class Recording(models.Model):
    narrator_name = models.CharField(max_length=100, null=True, blank=True)
    audio = models.FileField(upload_to=upload_location)
    timestamps = models.JSONField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recordings")

    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="recordings", null=True, blank=True)
    request = models.ForeignKey('RecordingRequest', on_delete=models.CASCADE, related_name="recordings", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user", "-created_at"]

class Narrator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="narrator")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="narrator", null=True, blank=True)
    narratorName = models.CharField(max_length=200)

    def __str__(self):
        return f"Narrator : {self.narratorName}"
    
class CombinedNarrations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="combined")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="combined", null=True, blank=True)
    narratorName = models.ForeignKey("Narrator", on_delete=models.CASCADE, related_name="combined")
    finalVideo = models.FileField(upload_to='upload_video')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["book", "created_at"]


class CombineVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comvideo")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="comvideo", null=True, blank=True)
    pages = models.FileField(upload_to=upload_video)
    audio = models.FileField(upload_to=upload_location)
    narrator = models.ForeignKey("Narrator", on_delete=models.CASCADE, related_name="comvideo")



