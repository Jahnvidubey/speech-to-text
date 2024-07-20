# speech/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import whisper
import os
import librosa
from django.http import HttpResponse

class UploadAudioFileView(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')  # Ensure this key matches the one used in your React code
        file_urls = []

        for file in files:
            file_path = default_storage.save('temp/' + file.name, ContentFile(file.read()))
            file_url = default_storage.url(file_path)
            file_urls.append({"file_path": file_path, "file_url": file_url})

        return Response(file_urls, status=status.HTTP_201_CREATED)

class RetrieveAudioFileView(APIView):
    def get(self, request, *args, **kwargs):
        files = default_storage.listdir('temp/')[1]  # List files in 'temp/' directory
        return Response(files, status=status.HTTP_200_OK)

class TranscribeAudioFileView(APIView):
    def get(self, request, file_path, *args, **kwargs):
        try:
            file_path = 'temp/' + file_path
            if not default_storage.exists(file_path):
                return Response({"error": "Audio file not found."}, status=status.HTTP_404_NOT_FOUND)

            # Load Whisper model
            model = whisper.load_model("base")

            # Ensure the audio file exists
            abs_file_path = default_storage.path(file_path)
            if not os.path.exists(abs_file_path):
                return Response({"error": "Audio file not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Transcribe the audio file using Whisper
            audio, sr = librosa.load(abs_file_path, sr=16000)
            result = model.transcribe(audio)
            transcription_text = result["text"]

            # Create a downloadable text file
            response = HttpResponse(transcription_text, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}.txt"'
            default_storage.delete(file_path)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
