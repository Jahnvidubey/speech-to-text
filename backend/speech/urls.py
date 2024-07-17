# urls.py

from django.urls import path
from .views import (
    UploadAudioFileView,
    RetrieveAudioFileView,
    TranscribeAudioFileView,
    DownloadIndividualFileView,
)

urlpatterns = [
    path('upload/', UploadAudioFileView.as_view(), name='upload_audio_file'),
    path('retrieve/', RetrieveAudioFileView.as_view(), name='retrieve_audio_file'),
    path('transcribe/<str:file_path>/', TranscribeAudioFileView.as_view(), name='transcribe_audio_file'),
    path('download/<str:file_path>/', DownloadIndividualFileView.as_view(), name='download_individual_file'),
]