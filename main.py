import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

AZURE_FACE_KEY = os.getenv('AZURE_FACE_KEY')
AZURE_FACE_ENDPOINT = os.getenv('AZURE_FACE_ENDPOINT')

def detect_face(url):
    face_client = FaceClient(AZURE_FACE_ENDPOINT, CognitiveServicesCredentials(AZURE_FACE_KEY))

    detected_faces = face_client.face.detect_with_url(url = url, detection_model='detection_03')
    if not detected_faces:
        print(f'No face detected in {url}')
        return
    
    for face in detected_faces:
        print(f'Face deteced, id={face.face_id}')


