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
# from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
from webconfig import AIFace

# Create an authenticated FaceClient.
face_client = FaceClient(
    AIFace.ENDPOINT, CognitiveServicesCredentials(AIFace.KEY))


def get_face_index(photo_path):
    # Detect a face in an image that contains a single face
    single_face_image_url = photo_path
    single_image_name = os.path.basename(single_face_image_url)
    # We use detection model 3 to get better performance.
    detected_faces = face_client.face.detect_with_url(
        url=single_face_image_url, detection_model='detection_03')
    if not detected_faces:
        raise Exception(
            'No face detected from image {}'.format(single_image_name))

    # Display the detected face ID in the first single-face image.
    # Face IDs are used for comparison to faces (their IDs) detected in other images.
    print('Detected face ID from', single_image_name, ':')
    for face in detected_faces:
        face_index = face.face_id
        print(face.face_id)
    return face_index


# def match_face_indexs(first_index):
#     # Detect the faces in an image that contains multiple faces
#     # Each detected face gets assigned a new ID
#     multi_face_image_url = "https://media.npr.org/assets/img/2018/02/13/ap_18043717687430-20-4964b394d87b24080f470f41af2ab3c4495d1e34-s800-c85.jpg"
#     multi_image_name = os.path.basename(multi_face_image_url)
#     # We use detection model 3 to get better performance.
#     detected_faces2 = face_client.face.detect_with_url(
#         url=multi_face_image_url, detection_model='detection_03')

#     # Search through faces detected in group image for the single face from first image.
#     # First, create a list of the face IDs found in the second image.
#     second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
#     # Next, find similar face IDs like the one detected in the first image.
#     similar_faces = face_client.face.find_similar(
#         face_id=first_index, face_ids=second_image_face_IDs)
#     if not similar_faces:
#         print('No similar faces found in', multi_image_name, '.')
#     # Print the details of the similar faces detected
#     else:
#         print('Similar faces found in', multi_image_name + ':')
#         for face in similar_faces:
#             first_image_face_ID = face.face_id
#             # The similar face IDs of the single face image and the group image do not need to match,
#             # they are only used for identification purposes in each image.
#             # The similar faces are matched using the Cognitive Services algorithm in find_similar().
#             face_info = next(
#                 x for x in detected_faces2 if x.face_id == first_image_face_ID)
#             if face_info:
#                 print('  Face ID: ', first_image_face_ID)
#                 print('  Face rectangle:')
#                 print('    Left: ', str(face_info.face_rectangle.left))
#                 print('    Top: ', str(face_info.face_rectangle.top))
#                 print('    Width: ', str(face_info.face_rectangle.width))
#                 print('    Height: ', str(face_info.face_rectangle.height))


# def save_index_into_photo():
#     # Detect a face in an image that contains a single face
#     single_face_image_url = 'https://media.npr.org/assets/img/2018/02/13/ap_18043717687430-20-4964b394d87b24080f470f41af2ab3c4495d1e34-s800-c85.jpg'
#     single_image_name = os.path.basename(single_face_image_url)
#     # We use detection model 3 to get better performance.
#     detected_faces = face_client.face.detect_with_url(
#         url=single_face_image_url, detection_model='detection_03')
#     if not detected_faces:
#         raise Exception(
#             'No face detected from image {}'.format(single_image_name))

#     # Convert width height to a point in a rectangle
#     def getRectangle(faceDictionary):
#         rect = faceDictionary.face_rectangle
#         left = rect.left
#         top = rect.top
#         right = left + rect.width
#         bottom = top + rect.height

#         return ((left, top), (right, bottom))

#     # Download the image from the url
#     response = requests.get(single_face_image_url)
#     img = Image.open(BytesIO(response.content))

#     # For each face returned use the face rectangle and draw a red box.
#     print('Drawing rectangle around face... see popup for results.')
#     draw = ImageDraw.Draw(img)
#     for face in detected_faces:
#         draw.rectangle(getRectangle(face), outline='red')
#         draw.text((getRectangle(face)[0][0]-20,
#                    getRectangle(face)[0][1]-10), face.face_id)

#     # Display the image in the users default image browser.
#     img.show()
#     # Save the image
#     img.save("test.jpg")
