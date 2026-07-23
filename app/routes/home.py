from flask import Blueprint, render_template
from app import mongo

home_bp = Blueprint("home", __name__)

@home_bp.route("/home")
def home():
    total = mongo.db.employees.count_documents({})
    departments = sorted([d for d in mongo.db.employees.distinct("department") if d])
    return render_template("home.html", total=total, departments=departments)
