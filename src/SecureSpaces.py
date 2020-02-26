from os import listdir
from os.path import isfile, join
import face_recognition
import sys
import cv2
import numpy as np
import PhoneMessaging.send_mms as SMS
from firebase import Firebase
from datetime import datetime
import threading
import time
from pathlib import Path
import asyncio
import threading
import urllib.request
from PIL import Image

config = {
    "apiKey": "AIzaSyCIb7b77N60HaFsUwsxuiiRJMtUfoC0ubs",
    "authDomain": "spaces-f099d.firebaseapp.com",
    "databaseURL": "https://spaces-f099d.firebaseio.com",
    "storageBucket": "spaces-f099d.appspot.com"
}

firebase = Firebase(config)

storage = firebase.storage()

db = firebase.database()

def cropImage(left, upper, right, lower, frame):
    intruder = Image.open(frame)
    box = (left, upper, right, lower)
    intruder_crop = intruder.crop((left, upper, right, lower))
    intruder_crop.save("./temp/"+frame, quality=95)
    storage.child("tmp/"+frame).put("./temp/"+frame)
    url = storage.child("tmp/"+frame).get_url("")
    message = SMS.Message("Intruder!")
    message.sendMessage(url)

def isInStrArray(strArray, string):
    for string_check in strArray:
        if string_check == string:
            return True
    return False

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
class Person:
    hasSentSMS = False
    def __init__(self, imageFile, faceName):
        self.faceName = faceName
        self.image = face_recognition.load_image_file(imageFile)
        self.image_face_encoding = face_recognition.face_encodings(self.image)[0] 
    def flipSentSMS(self):
        self.hasSentSMS = True

def imageIDIsInArray(givenArray, givenID):
    for id_user in givenArray:
        if id_user == givenID:
            return True
    return False


class Faces(threading.Thread):
    friends = [f for f in listdir("friends") if isfile(join("friends", f)) ]
    intruders = [f for f in listdir("intruders") if isfile(join("intruders", f)) ]
    personArray = []
    friendsArrayImage = []
    friendsArrayName = []
    intrudersArrayImage = []
    intrudersArrayName = []
    imageIDArray = []
    def updateDatabase(self):
        isUpdated = False
        all_users = db.child("authorized").get()
        index = 0
        for user in all_users.each():
            if (imageIDIsInArray(self.imageIDArray, user.val()["imageId"]) == False):
                self.imageIDArray.append(user.val()["imageId"])
                url = storage.child(user.val()["imageId"]).get_url("")
                #print(url)
                urllib.request.urlretrieve(url, "friends/friends%d.jpg" % index)
                index += 1
                isUpdated = True
        all_users = db.child("intruders").get()
        index = 0
        for user in all_users.each():
            if (imageIDIsInArray(self.imageIDArray, user.val()["imageId"]) == False):
                self.imageIDArray.append(user.val()["imageId"])
                url = storage.child(user.val()["imageId"]).get_url("")
                urllib.request.urlretrieve(url, "intruders/intruder%d.jpg" % index)
                index += 1
                isUpdated = True
        if isUpdated:
            for friend in self.friends:
                self.friendsArrayImage.append("./friends/"+ friend)
                self.friendsArrayName.append("Authorized")
            for intruder in self.intruders:
                self.intrudersArrayImage.append("./intruders/"+ intruder)
                self.intrudersArrayName.append("Intruder " + str(len(self.intrudersArrayName)))
        '''
        for user in all_users.each():
            if imageIDIsInArray(self.imageIDArray,user.val()["imageId"]) == False:
                isUpdated = True
                self.imageIDArray.append(user.val()["imageId"])
                url = storage.child(user.val()["imageId"].split(".")[0]).get_url("")
                urllib.request.urlretrieve(url, "intruders/intruders.jpg")
        all_users = db.child("authorized").get()
        for user in all_users.each():
            if imageIDIsInArray(self.imageIDArray,user.val()["imageId"]) == False:
                isUpdated = True
                self.imageIDArray.append(user.val()["imageId"])
                url = storage.child(user.val()["imageId"].split(".")[0]).get_url("")
                urllib.request.urlretrieve(url, "friends/Jamie.jpg")
        if isUpdated:
            for friend in self.friends:
                self.friendsArrayImage.append("./friends/"+ friend)
                self.friendsArrayName.append("Authorized")
            for intruder in self.intruders:
                self.intrudersArrayImage.append("./intruders/"+ intruder)
                self.intrudersArrayName.append("Intruder" + str(len(self.intrudersArrayName)))
        '''
# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)
#Add everyone to a persons array
#personArray = [zeak, kyle]


allFaces = Faces()
allFaces.updateDatabase()
friendsOnly = False;
if len(sys.argv) == 2 and sys.argv[1] == 'S':
    friendsOnly = True

#for friend in allFaces.friends:
    #personArray.append(Person("./"+ friendsDir +"/"+ friend, "friend"))

#for intruder in allFaces.intruders:
    #personArray.append(Person("./"+ intruderDir +"/"+ intruder, "Intruder"))

def sendIntruderMessage():
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = SMS.Message(dt_string + " - " + " Intruder!")
    message.sendMessage()

video_capture = cv2.VideoCapture(0)


# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
#for person in allFaces.personArray:
#known_face_encodings.append(person.image_face_encoding)
#known_face_names.append(person.faceName)
#known_face_encodings = [obama_face_encoding, biden_face_encoding]
#known_face_names = ["Zeak","Intruder"]




def updateImages(imageFile, name):
    imageNew = face_recognition.load_image_file(imageFile)
    image_face_encoding = face_recognition.face_encodings(imageNew)[0]
    known_face_names.append(name)
    known_face_encodings.append(image_face_encoding)

index = 0

#image = face_recognition.load_image_file(allFaces.friendsArrayImage[0])
#face_recognition.face_encodings(image)
def updateArrays():
    index = 0
    for face, name in zip(allFaces.friendsArrayImage, allFaces.friendsArrayName):
        updateImages(face, name)
        index += 1
    index = 0

    for face, name in zip(allFaces.intrudersArrayImage, allFaces.intrudersArrayName):
        updateImages(face, name)
        index += 1

updateArrays()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
friendsOnlyIntruder = False
alreadySentSMSIntruders = []
alreadySentSMSUnknown = []
frameCount  = 0
while True:
    frameCount += 1
    if (frameCount > 100):
        print("Updating Database...")
        allFaces.updateDatabase()
        updateArrays()
        print("Done")
        frameCount = 0

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if (name == "Intruder"):
                if personArray[best_match_index].hasSentSMS == False:
                    personArray[best_match_index].flipSentSMS()
                    #sendIntruderMessage()
            if (friendsOnly and name == "Unknown" and friendsOnlyIntruder == False):
                #sendIntruderMessage()
                friendsOnlyIntruder = True
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if ("Intruder" in name):
            if isInStrArray(alreadySentSMSIntruders, name) == False:
                alreadySentSMSIntruders.append(name)
                cv2.imwrite("frame.jpg", frame)     # save frame as JPEG file
                cropImage(left - 100, top - 100, right + 100, bottom + 100, "frame.jpg")
        if (name == "Unknown" and friendsOnly):
            if isInStrArray(alreadySentSMSIntruders, name) == False:
                nameOfUk = name + str(len(alreadySentSMSUnknown))               
                alreadySentSMSUnknown.append(nameOfUk)
                cv2.imwrite(nameOfUk + ".jpg", frame)
                cropImage(left - 100, top - 100, right + 100, bottom + 100, nameOfUk + ".jpg") 
                ukimage = face_recognition.load_image_file(nameOfUk + ".jpg")
                ukimage_face_encoding = face_recognition.face_encodings(ukimage)[0]
                known_face_encodings.append(ukimage_face_encoding)
                known_face_names.append(nameOfUk)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
