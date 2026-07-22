from flask import Blueprint, request, redirect, url_for, render_template
from bson.objectid import ObjectId  # for handling MongoDB _id
from app import mongo  # your PyMongo instance from __init__.py

employee_bp = Blueprint("employee", __name__)

# Helper function to convert MongoDB document _id to a string id for templates
def convert_doc(doc):
    """Convert MongoDB document: add 'id' field with string version of _id."""
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
    return doc

# Routes that don't use the database (keep as is)
@employee_bp.route("/employee/<int:id>/<string:name>")
def searchByNameId(id, name):
    return f"ID : {id} Name : {name}"

@employee_bp.route("/employee")
def displaySpecific():
    department = request.args.get("department")
    page = request.args.get("page")
    return f"Department : {department} Page : {page}"

@employee_bp.route("/employeeDepartment")
def gotodept():
    return redirect(url_for("department.departmentHome"))

@employee_bp.route("/employee/register")
def register_employee():
    return render_template("add_employee.html")

# CRUD routes – now using MongoDB

# List all employees
@employee_bp.route("/employee/list")
def employee_list():
    # Get all documents from the 'employees' collection
    employees_cursor = mongo.db.employees.find()
    # Convert each document to add an 'id' field
    employees = [convert_doc(emp) for emp in employees_cursor]
    return render_template("employee.html", employees=employees)

# Add employee (POST) or show form (GET)
@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():
    if request.method == "POST":
        # Build the employee document from form data
        new_employee = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
            "salary": request.form["salary"],
            "department": request.form["department"]
        }
        # Insert into MongoDB
        mongo.db.employees.insert_one(new_employee)
        return redirect(url_for("employee.employee_list"))
    
    return render_template("add_employee.html")

# Get a single employee by ID (MongoDB ObjectId)
@employee_bp.route("/employee/employeeDetail/<id>", methods=["GET"])
def employeeDetail(id):
    # Use ObjectId to find by _id
    employee = mongo.db.employees.find_one({"_id": ObjectId(id)})
    if not employee:
        # If not found, return 404 – you can raise abort(404) or render a 404 page
        return render_template("404.html"), 404
    employee = convert_doc(employee)
    return render_template("employee_detail.html", employee=employee)

# Update employee (POST) or show update form (GET)
@employee_bp.route("/employee/employeeUpdate/<id>", methods=["POST", "GET"])
def employeeUpdate(id):
    employee = mongo.db.employees.find_one({"_id": ObjectId(id)})
    if not employee:
        return render_template("404.html"), 404
    
    if request.method == "POST":
        # Update fields
        update_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
            "salary": request.form["salary"],
            "department": request.form["department"]
        }
        # Update the document
        mongo.db.employees.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return redirect(url_for("employee.employee_list"))
    
    employee = convert_doc(employee)
    return render_template("update_employee.html", employee=employee)

# Delete employee
@employee_bp.route("/employee/employeeDelete/<id>")
def employeeDelete(id):
    result = mongo.db.employees.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        # No document found – handle gracefully
        return render_template("404.html"), 404
    return redirect(url_for("employee.employee_list"))

# ------------------------------------------------------------
# (Optional) Advanced features: pagination, filtering, searching
# You can add them later using MongoDB's aggregate, skip, limit, etc.
# ------------------------------------------------------------