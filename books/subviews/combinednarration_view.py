from books.models import CombineVideo
from books.serializers import CombineVideoSerializer, RecordingSerializer
from moviepy.editor import *
from moviepy.audio import *
import tempfile
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import time
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import transaction
from bedtime.pagination import CustomPagination
from books.models import Page


class CombinedNarration(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CombineVideoSerializer
    combinedSerializer = RecordingSerializer
    def create(self, request, *args, **kwargs):
        user = self.request.user
        combined = CombineVideo.objects.filter(book = request.data['book'], user = user)
        ### input : {user, bookId, narrator, pagesUrl={1,2,3}, audioUrl = {1,2,3}}
        ### output: Store each data in CombineVideo and get the urls from CombineVideo and process
        ### the video and audio to store in CombinedNarrations
        
        temp_dir = tempfile.mkdtemp()

        for num, obj in enumerate(combined):
            videoClip = VideoFileClip(obj.pages.url[1:])
            audioClip = AudioFileClip(obj.audio.url[1:])

            audioLength = audioClip.duration
            clipCutoff = 12

            if audioLength < clipCutoff:
                videoClip = videoClip.subclip(0, clipCutoff)
                final_audio = (CompositeAudioClip([videoClip.audio, audioClip]))
                final_audio = final_audio.audio_fadeout(2)
                final_clip = videoClip.set_audio(final_audio)
                

            elif audioLength <= 20:
                videoClip = videoClip.subclip(0, audioLength)
                final_audio = CompositeAudioClip([videoClip.audio, audioClip])
                final_audio = final_audio.audio_fadeout(2)
                final_clip = videoClip.set_audio(final_audio)
                
            output_path = os.path.join(temp_dir, f"combined{num}.mp4")
            final_clip.write_videofile(output_path)
        
        video_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
        video_clips = [VideoFileClip(os.path.join(temp_dir, file)) for file in video_files]
        final_video = concatenate_videoclips(video_clips, method="compose")
        output_path = os.path.join(temp_dir, "finalCombinedVideo.mp4")
        final_video.write_videofile(output_path)

        narratorName = request.data['narrator']
        with open(output_path, 'rb') as video_file:
            uploaded_file = SimpleUploadedFile('finalVideo.mp4', video_file.read(), content_type='multipart/form-data')

        print("Output Path ==> ", output_path)
        data = {
            'user':user.id,
            'book':request.data.get('book'),
            'timestamps':time.time.now(),
            'narrator_name':narratorName,
            'finalVideo': uploaded_file
        }

        combined_serializer = RecordingSerializer(data=data)
        if combined_serializer.is_valid():
            combined_serializer.save()
            return JsonResponse({"status": "success"})
        else:
            print(combined_serializer.errors)
            return JsonResponse({"status": "error", "errors": combined_serializer.errors})
