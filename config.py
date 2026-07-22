import os
#It contains 
# configuration things like : URL, API, secrectKey, database url

class Config:

    SECRECT_KEY = "sha256"
    MONGO_URI = "mongodb+srv://abhinavin07:QHVgOjDsIeVG5x2U@cluster0.avermlt.mongodb.net/employee_db?retryWrites=true&w=majority"
    
    SQLALCHEMY_TRACK_MODIFICATION = False

    APP_NAME = "Employee Management System"
    UPLOAD_FOLDER = "uploads"
    API_KEY = "12341asdasd"
    DEBUG = True