# from django.urls import path
# from .views import UploadAudioFileView, RetrieveAudioFileView, TranscribeAudioFileView

# urlpatterns = [
#     path('upload/', UploadAudioFileView.as_view(), name='upload_audio'),
#     path('retrieve/<uuid:id>/', RetrieveAudioFileView.as_view(), name='retrieve_audio'),
#     path('transcribe/<uuid:id>/', TranscribeAudioFileView.as_view(), name='transcribe_audio'),
# ]

# speech/urls.py

from django.urls import path
from .views import UploadAudioFileView, RetrieveAudioFileView, TranscribeAudioFileView

urlpatterns = [
    path('upload/', UploadAudioFileView.as_view(), name='upload_audio'),
    path('retrieve/', RetrieveAudioFileView.as_view(), name='retrieve_all_audio'),
    path('transcribe/<path:file_path>/', TranscribeAudioFileView.as_view(), name='transcribe_audio'),
]
