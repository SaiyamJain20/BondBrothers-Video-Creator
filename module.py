import cv2
import numpy as np
from datetime import datetime

class User:
    def __init__(self, name, username, email, password, id=-1, isAdmin="False"):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        
    def printUser(self):
        if (self != None):
            print("User ID:", self.id)
            print("Name:", self.name)
            print("Username:", self.username)
            print("Email:", self.email)
            print("Password:", self.password)
            print("Is Admin:", self.isAdmin)
        else:
            print("User not found.")
        
    def UploadData(self, cursor):
        cursor.execute("INSERT INTO Users (name, username, email, password, isAdmin) VALUES (%s, %s, %s, %s, %s)", (self.name, self.username, self.email, self.password, self.isAdmin))
 
class Image:
    def __init__(self, file_name, image_len, file_type, file_data, upload_date = datetime.now()):
        self.file_name = file_name
        self.file_size = image_len
        self.file_type = file_type
        self.file_data = file_data
        self.upload_date = upload_date
        
    def display(self):
        nparr = np.frombuffer(self.file_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow(self.file_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
 
class Audio:
    def __init__(self, file_name, file_size, file_type, file_data, duration, upload_date = datetime.now()):
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type
        self.file_data = file_data
        self.duration = duration
        self.upload_date = upload_date       
 