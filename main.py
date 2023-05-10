# import the opencv library
import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("ServiseAccounttKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendence-d891c-default-rtdb.firebaseio.com",
    'storageBucket': "faceattendence-d891c.appspot.com"
})

bucket = storage.bucket()



# define a video capture object
vid = cv2.VideoCapture(0)
vid .set(3, 640)
vid .set(4, 480)

# path
imgbackground = cv2. imread(r'C:\Users\harsh\PycharmProjects\face attendence system\Resources\background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))


# Load the encoding file
import pickle
import os.path

filename = 'EncodeFile.p'

if not os.path.exists(filename) or os.path.getsize(filename) == 0:
    print("Error: File doesn't exist or is empty")
else:
    print("Loading Encode File ...")
    with open(filename, 'rb') as file:
        try:
            encodeListKnownWithIds = pickle.load(file)
            encodeListKnown, studentIds = encodeListKnownWithIds
            # print(studentIds)
        except (pickle.UnpicklingError, EOFError):
            print("Error: Failed to unpickle data from the file")


modeType = 0
counter = 0
id = -1
imgStudent = []



while (True):

    # Capture the video frame
    # by frame
    ret, img = vid.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgbackground[162:162 + 480, 55:55 + 640] = img
    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType= 1


        if counter!= 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType =3
                counter = 0
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


            if modeType != 3:

              if 10 < counter < 20:
                modeType = 2

              imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

              if counter <= 10:
                cv2.putText(imgbackground, str(studentInfo['total_attendance']), (861,125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                cv2.putText(imgbackground, str(studentInfo['major']), (1006, 550),
                             cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imgbackground, str(id), (1006, 493),
                             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgbackground, str(studentInfo['standing']), (910, 625),
                             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgbackground, str(studentInfo['year']), (1025, 625),
                             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgbackground, str(studentInfo['starting_year']), (1125, 625),
                             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1 )

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgbackground, str(studentInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgbackground[175:175 + 216, 909:909 + 216] = imgStudent

    counter += 1

    if counter >= 20:
        counter = 0
        modeType = 0
        studentInfo = []
        imgStudent = []
        imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
else:
        modeType = 0
        counter = 0












    # Display the resulting frame


    #  cv2.imshow('frame', img)
        cv2.imshow('Face Attendence', imgbackground)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
        cv2.waitKey(1)