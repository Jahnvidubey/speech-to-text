from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from .utils import convert_to_abbreviation
import whisper
import contractions
import os
import librosa
import zipfile
import io

def index(request):
    return render(request, 'speechapp/index.html')

class UploadAudioFileView(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
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

class CustomFileResponse(FileResponse):
    def __init__(self, *args, **kwargs):
        self.file_to_delete = kwargs.pop('file_to_delete', None)
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()
        if self.file_to_delete and os.path.exists(self.file_to_delete):
            os.remove(self.file_to_delete)

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

            # Expand contractions and convert to abbreviations
            transcription_text = contractions.fix(transcription_text)
            transcription_text = convert_to_abbreviation(transcription_text)

            # Save transcription text to a file in 'temp/' directory
            transcription_file_name = os.path.basename(file_path) + ".txt"
            transcription_file_path = 'temp/' + transcription_file_name
            with default_storage.open(transcription_file_path, 'w') as transcription_file:
                transcription_file.write(transcription_text)

            # Create a downloadable text file response
            response = CustomFileResponse(open(default_storage.path(transcription_file_path), 'rb'),
                                          content_type='text/plain',
                                          file_to_delete=default_storage.path(transcription_file_path))
            response['Content-Disposition'] = f'attachment; filename="{transcription_file_name}"'

            # Clean up the original audio file
            default_storage.delete(file_path)

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadIndividualFileView(APIView):
    def get(self, request, file_path, *args, **kwargs):
        try:
            file_path = 'temp/' + file_path
            # Check if file exists
            if not default_storage.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            # Open the file and prepare the response (assuming it's an audio file)
            abs_file_path = default_storage.path(file_path)
            response = FileResponse(open(abs_file_path, 'rb'), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'

            return response

        except Exception as e:
            return Response({"error": "An error occurred during download."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
