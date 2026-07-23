from flask import Blueprint, request, redirect, url_for, render_template, flash
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

# List all employees with combined search, filtering, sorting, and pagination
@employee_bp.route("/employee/list")
def employee_list():
    PER_PAGE = 5
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    dept = request.args.get("dept", "").strip()
    min_salary = request.args.get("min_salary", type=int)
    max_salary = request.args.get("max_salary", type=int)

    # Sorting
    sort_by = request.args.get("sort_by", "name")
    sort_dir = request.args.get("sort_dir", "asc")
    allowed_sort_fields = ["name", "email", "department", "salary"]

    if sort_by not in allowed_sort_fields:
        sort_by = "name"
    if sort_dir not in ["asc", "desc"]:
        sort_dir = "asc"

    mongo_sort_dir = 1 if sort_dir == "asc" else -1

    if page < 1:
        page = 1

    # Get unique departments from database
    departments = mongo.db.employees.distinct("department")
    departments = sorted([d for d in departments if d])

    # Build single filter_conditions dictionary with all filters
    filter_conditions = {}

    # Search filter
    if search:
        filter_conditions["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"department": {"$regex": search, "$options": "i"}}
        ]

    # Department filter
    if dept:
        filter_conditions["department"] = dept

    # Salary range filter
    if min_salary is not None and min_salary >= 0:
        filter_conditions["salary"] = filter_conditions.get("salary", {})
        filter_conditions["salary"]["$gte"] = min_salary
    if max_salary is not None and max_salary >= 0:
        filter_conditions["salary"] = filter_conditions.get("salary", {})
        filter_conditions["salary"]["$lte"] = max_salary

    # Get total count for pagination
    total = mongo.db.employees.count_documents(filter_conditions)
    total_pages = (total + PER_PAGE - 1) // PER_PAGE

    # Apply filter -> sort -> skip -> limit
    employees_cursor = (
        mongo.db.employees.find(filter_conditions)
        .sort([(sort_by, mongo_sort_dir)])
        .skip((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
    )
    employees = [convert_doc(emp) for emp in employees_cursor]

    return render_template(
        "employee.html",
        employees=employees,
        page=page,
        total_pages=total_pages,
        total=total,
        per_page=PER_PAGE,
        search=search,
        sort_by=sort_by,
        sort_dir=sort_dir,
        dept=dept,
        departments=departments,
        min_salary=min_salary,
        max_salary=max_salary
    )

# Add employee (POST) or show form (GET)
@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():
    departments = sorted([d for d in mongo.db.employees.distinct("department") if d])
    
    if request.method == "POST":
        try:
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
            flash("Employee added successfully!", "success")
            return redirect(url_for("employee.employee_list"))
        except Exception as e:
            flash(f"Failed to add employee: {str(e)}", "danger")
    
    return render_template("add_employee.html", departments=departments)

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
    departments = sorted([d for d in mongo.db.employees.distinct("department") if d])
    
    if not employee:
        flash("Employee not found.", "danger")
        return redirect(url_for("employee.employee_list"))
    
    if request.method == "POST":
        try:
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
            flash("Employee updated successfully!", "success")
            return redirect(url_for("employee.employee_list"))
        except Exception as e:
            flash(f"Failed to update employee: {str(e)}", "danger")
    
    employee = convert_doc(employee)
    return render_template("update_employee.html", employee=employee, departments=departments)

# Delete employee
@employee_bp.route("/employee/employeeDelete/<id>")
def employeeDelete(id):
    try:
        result = mongo.db.employees.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            flash("Employee not found.", "warning")
            return redirect(url_for("employee.employee_list"))
        flash("Employee deleted successfully!", "success")
    except Exception as e:
        flash(f"Failed to delete employee: {str(e)}", "danger")
    return redirect(url_for("employee.employee_list"))

# ------------------------------------------------------------
# (Optional) Advanced features: pagination, filtering, searching
# You can add them later using MongoDB's aggregate, skip, limit, etc.
# ------------------------------------------------------------