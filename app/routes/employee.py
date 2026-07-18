from flask import Blueprint, request, redirect, url_for, render_template

from app.models.employee import Employee

employee_bp = Blueprint("employee", __name__)

# @employee_bp.route("/employee_home")
# def employee_list():
#     return "Employee List"

# @employee_bp.route("/employee/add")
# def add_employee():
#     return "Add Employee"

# @employee_bp.route("/employee/update")
# def update_employee():
#     return "Update Employee"

# @employee_bp.route("/employee/delete")
# def delete_employee():
#     return "Delete Employee"

# @employee_bp.route("/employee/<int:id>")
# def getEmployeebyId(id):
#     return f"Employee : {id}"

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

@employee_bp.route("/employee/register")
def register_employee():

    return render_template("add_employee.html")

@employee_bp.route("/employee/list")
def employee_list():

    employees = Employee.query.all()

    return render_template("employee.html", employees = employees)


from app.models import db

@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():

    if request.method == "POST":

        employee = Employee(
            name = request.form["name"],
            email = request.form["email"],
            password = request.form["password"],
            salary = request.form["salary"],
            department = request.form["department"]
        )

        #database query
        db.session.add(employee)
        #run the query
        db.session.commit()

        return redirect(url_for("employee.employee_list"))
    
    return render_template("add_employee.html")

#get specific employee
@employee_bp.route("/employee/employeeDetail/<int:id>", methods=["GET"])
def employeeDetail(id):

    employee = Employee.query.get_or_404(id)

    return render_template("employee_detail.html", employee = employee)


@employee_bp.route("/employee/employeeUpdate/<int:id>", methods=["POST", "GET"])
def employeeUpdate(id):

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":

        employee.name = request.form["name"]
        employee.email = request.form["email"]
        employee.password = request.form["password"]
        employee.salary = request.form["salary"]
        employee.department = request.form["department"]

        db.session.commit()

        return redirect(url_for("employee.employee_list"))

    return render_template("update_employee.html", employee=employee)


@employee_bp.route("/employee/employeeDelete/<int:id>")
def employeeDelete(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for("employee.employee_list"))

#advance crud operation

#pagination
#sorting
#filtering
#searching
