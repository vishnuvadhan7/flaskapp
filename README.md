# Employee Management System (EMS)

A full-featured Flask web application for managing employee records with MongoDB database. Built with Bootstrap 5 for a modern, responsive UI.

---

## Features

### Core Operations
- **Create** - Add new employees with name, email, password, salary, and department
- **Read** - View employee list with details and search functionality
- **Update** - Edit existing employee information
- **Delete** - Remove employees with confirmation dialog

### Data Management
- **Pagination** - 5 employees per page with Previous/Next navigation
- **Search** - Search by name, email, or department (case-insensitive)
- **Sorting** - Sort by name, email, department, or salary (ascending/descending)
- **Filtering** - Filter by department dropdown and salary range (min/max)

### User Interface
- Bootstrap 5 responsive design
- Flash messages for user feedback (success/error)
- Sort indicators (▲/▼) on column headers
- Clean card-based layout
- Empty state for no results

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Backend | Flask |
| Database | MongoDB (PyMongo) |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap 5 |
| Icons | Bootstrap Icons |

---

## Prerequisites

- **Python** 3.8 or higher
- **MongoDB** - Local or Atlas cloud instance
- **Git** - For cloning the repository

Check your Python version:
```bash
python --version
```

---

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd Flask-Development
```

### 2. Create Virtual Environment

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

Edit `config.py` to configure your MongoDB connection:

```python
class Config:
    SECRET_KEY = "your-secret-key"
    
    # Replace with your MongoDB connection string
    # For local MongoDB: "mongodb://localhost:27017/employee_db"
    # For MongoDB Atlas: "mongodb+srv://<username>:<password>@<cluster>/<dbname>?retryWrites=true&w=majority"
    MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/employee_db?retryWrites=true&w=majority"
    
    DEBUG = True
```

### MongoDB Atlas Setup (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster (free tier)
3. Create a database user
4. Whitelist your IP address (0.0.0.0 for development)
5. Get your connection string and update `config.py`

---

## Running the Application

```bash
python app.py
```

Or with Flask CLI:
```bash
flask run
```

The application will start at: **http://127.0.0.1:5000**

---

## Usage Guide

### Navigation
- **Home** - Welcome page
- **Employee List** - View all employees with filters
- **Add Employee** - Create new employee record
- **Departments** - View department information

### Search
Enter a search term in the search box to find employees by:
- Name
- Email
- Department

Example: `/employee/list?search=john`

### Sorting
Click column headers to sort:
- Name (A-Z / Z-A)
- Department (A-Z / Z-A)
- Salary (Low to High / High to Low)
- Email (A-Z / Z-A)

Example: `/employee/list?sort_by=salary&sort_dir=desc`

### Filtering

**By Department:**
Select a department from the dropdown.

Example: `/employee/list?dept=IT`

**By Salary Range:**
Enter minimum and/or maximum salary values.

Example: `/employee/list?min_salary=50000&max_salary=100000`

### Combining Filters
All filters work together:

```
/employee/list?search=john&dept=IT&min_salary=50000&sort_by=salary&sort_dir=desc&page=2
```

---

## Project Structure

```
Flask-Development/
├── app/
│   ├── models/          # Data models
│   │   └── employee.py
│   ├── routes/          # Route handlers (blueprints)
│   │   ├── employee.py
│   │   ├── department.py
│   │   └── home.py
│   ├── templates/       # HTML templates
│   │   ├── base.html
│   │   ├── employee.html
│   │   ├── macros.html
│   │   └── ...
│   ├── static/          # CSS, JS, images
│   │   ├── css/
│   │   └── js/
│   └── utils/           # Utility functions
├── config.py            # Configuration settings
├── app.py               # Application entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirect to home |
| GET | `/home` | Home page |
| GET | `/employee/list` | Employee list with filters |
| GET/POST | `/employee/add` | Add new employee |
| GET | `/employee/employeeDetail/<id>` | View employee details |
| GET/POST | `/employee/employeeUpdate/<id>` | Edit employee |
| GET | `/employee/employeeDelete/<id>` | Delete employee |
| GET | `/department` | Department page |

---

## Screenshots

> Add screenshots here by placing images in the `docs/` folder and referencing them:
> 
> ![Employee List](docs/employee-list.png)
> ![Add Employee](docs/add-employee.png)

---

## Troubleshooting

### MongoDB Connection Errors
- Verify your MONGO_URI in `config.py`
- Check MongoDB Atlas network access settings
- Ensure MongoDB service is running (local)

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000
```

### Import Errors
Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Future Enhancements

- [ ] User authentication and login
- [ ] CSV export functionality
- [ ] Employee profile pictures
- [ ] Advanced search with filters
- [ ] Dashboard with charts
- [ ] REST API for mobile apps

---

## License

This project is for educational purposes.

---

## Author

**Your Name**
- GitHub: [your-github-username]
- Email: your-email@example.com

---

## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)

---

## Support

If you find this project helpful, please give it a ⭐ on GitHub!