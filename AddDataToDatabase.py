import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiseAccounttKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendence-d891c-default-rtdb.firebaseio.com/",
})

ref = db.reference('StudentIds')

data = {
   "225511":
        {
            "name": "Manish Gupta",
            "major": "student",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "11881":
        {
            "name": "Harsh Kasyap",
            "major": "AI developer",
            "starting_year": 2022,
            "total_attendance": 10,
            "standing": "H",
            "year": 1,
            "last_attendance_time": "2023-03-11 00:54:39"
        },

    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "321688":
        {
            "name": "onkar Gupta",
            "major": "Student",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "O",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)
