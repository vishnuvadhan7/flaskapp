from flask import Blueprint, request, redirect, url_for, render_template

employee_bp = Blueprint("employee", __name__)

# @employee_bp.route("/employee_home")
# def employee_list():
#     return "Employee List"

# @employee_bp.route("/employee/add")
# def add_employee():
#     return "Add Employee"

@employee_bp.route("/employee/update")
def update_employee():
    return "Update Employee"

@employee_bp.route("/employee/delete")
def delete_employee():
    return "Delete Employee"

@employee_bp.route("/employee/<int:id>")
def getEmployeebyId(id):
    return f"Employee : {id}"

@employee_bp.route("/employee/<int:id>/<string:name>")
def searchByNameId(id, name):
    return f"ID : {id} Name : {name}"

# query parameter : filtering/ sorting  ?

@employee_bp.route("/employee")
def displaySpecific():
    department = request.args.get("department")
    page = request.args.get("page")

    return f"Department : {department} Page : {page}"

@employee_bp.route("/employeeDepartment")
def gotodept():
    return redirect(url_for("department.departmentHome"))


# request 

# get and post

@employee_bp.route("/employee/register", methods=["POST"])
def register_employee():
    data = request.get_json();

    name = data["name"]
    department = data["department"]
    salary = data["salary"]

    return f"Name : {name} Deparment : {department} Salary : {salary}"

@employee_bp.route("/employee/list")
def employee_list():
    employees = [
        {
            "name" : "amit",
            "salary" : 40000,
            "department" : "IT"
        },
        {
            "name" : "vijay",
            "salary" : 40000,
            "department" : "R&D"
        },
        {
            "name" : "aman",
            "salary" : 40000,
            "department" : "Sales"
        }
    ]

    return render_template("employee.html", employees = employees)


employee_list = []

@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():

    if request.method == "POST":
        #take user details

        # name = request.form.get("name")
        # department = request.form.get("department")
        # salary = request.form.get("salary")

        employee = {
            "name" : request.form.get("name"),
            "department": request.form.get("department"),
            "salary" : request.form.get("salary")
        }

        employee_list.append(employee)

        return redirect(url_for("employee.employee_list"))


    return render_template("add_employee.html")
