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

DETECTION_MODEL = 'detection_03'
RECOGNITION_MODEL = 'recognition_04'

AZURE_FACE_KEY = os.getenv('AZURE_FACE_KEY')
AZURE_FACE_ENDPOINT = os.getenv('AZURE_FACE_ENDPOINT')

PERSON_GROUP_ID = 'family'
KID_PERSON_ID = os.getenv('KID_PERSON_ID')


def detect_face(url):
    face_client = get_face_client()

    detected_faces = face_client.face.detect_with_url(url = url, detection_model=DETECTION_MODEL)
    if not detected_faces:
        print('No face detected')
        return None
    
    for face in detected_faces:
        print(f'Face deteced, id={face.face_id}, {face.face_rectangle}')

    return face

def get_face_client():
    return FaceClient(AZURE_FACE_ENDPOINT, CognitiveServicesCredentials(AZURE_FACE_KEY))

def make_person_group():
    face_client = get_face_client()

    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID, recognition_model=RECOGNITION_MODEL)

    kid = face_client.person_group_person.create(PERSON_GROUP_ID, "Kid")
    print(f'Kid={kid}')
    husband = face_client.person_group_person.create(PERSON_GROUP_ID, "Husband")
    print(f'Husband={husband}')
    wife = face_client.person_group_person.create(PERSON_GROUP_ID, "Wife")
    print(f'Wife={wife}')

def register(id, url):
    print(f'URL={url}')
    face_client = get_face_client()
    face_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, id, url, detection_model=DETECTION_MODEL)

def register_kid():
    file = open('kid.txt', 'r')
    urls = file.readlines()
    for url in urls:
        register(KID_PERSON_ID, url.rstrip('\n'))
    file.close()

def train():
    face_client = get_face_client()
    face_client.person_group.train(PERSON_GROUP_ID)

def get_train_status():
    face_client = get_face_client()
    status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print(f'status={status}')
