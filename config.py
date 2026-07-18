#It contains 
# configuration things like : URL, API, secrectKey, database url

class Config:

    SECRECT_KEY = "sha256"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/employee_db"
    SQLALCHEMY_TRACK_MODIFICATION = False

    APP_NAME = "Employee Management System"
    UPLOAD_FOLDER = "uploads"
    API_KEY = "12341asdasd"
    DEBUG = True