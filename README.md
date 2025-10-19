# Task Management API

A Django REST Framework API for managing tasks with user authentication, filtering, and sorting capabilities.

## 🚀 Features

- **User Authentication**
  - User registration
  - Login with token authentication
  - Logout functionality

- **Task Management**
  - Create, Read, Update, Delete (CRUD) operations
  - Mark tasks as complete/incomplete
  - Filter tasks by status, priority, and due date
  - Sort tasks by due date or priority
  - Each user can only access their own tasks

- **Task Attributes**
  - Title
  - Description
  - Due Date (must be in the future)
  - Priority (Low, Medium, High)
  - Status (Pending, Completed)
  - Timestamps (created_at, updated_at, completed_at)

## 🛠️ Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite (development)
- Token Authentication

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/UbaniTheFirst/task_management_api.git
cd task_management_api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# source venv/bin/activate     # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📡 API Endpoints

### Authentication

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register/` | POST | Register new user | No |
| `/api/auth/login/` | POST | Login and get token | No |
| `/api/auth/logout/` | POST | Logout user | Yes |

### Tasks

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/tasks/` | GET | List all user's tasks | Yes |
| `/api/tasks/` | POST | Create new task | Yes |
| `/api/tasks/{id}/` | GET | Get task details | Yes |
| `/api/tasks/{id}/` | PUT | Update task | Yes |
| `/api/tasks/{id}/` | DELETE | Delete task | Yes |
| `/api/tasks/{id}/complete/` | PATCH | Mark task complete | Yes |
| `/api/tasks/{id}/incomplete/` | PATCH | Mark task incomplete | Yes |

## 🔍 API Usage Examples

### Register a New User
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "a1b2c3d4e5f6...",
  "message": "User registered successfully"
}
```

### Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "token": "a1b2c3d4e5f6...",
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

### Create a Task
```bash
POST /api/tasks/
Authorization: Token a1b2c3d4e5f6...
Content-Type: application/json

{
  "title": "Complete capstone project",
  "description": "Finish and submit the task management API",
  "due_date": "2025-10-25",
  "priority": "High"
}
```

**Response:**
```json
{
  "id": 1,
  "user": "john_doe",
  "title": "Complete capstone project",
  "description": "Finish and submit the task management API",
  "due_date": "2025-10-25",
  "priority": "High",
  "status": "Pending",
  "completed_at": null,
  "created_at": "2025-10-19T10:30:00Z",
  "updated_at": "2025-10-19T10:30:00Z"
}
```

### List All Tasks with Filtering
```bash
GET /api/tasks/?status=Pending&priority=High&ordering=due_date
Authorization: Token a1b2c3d4e5f6...
```

### Mark Task as Complete
```bash
PATCH /api/tasks/1/complete/
Authorization: Token a1b2c3d4e5f6...
```

**Response:**
```json
{
  "id": 1,
  "user": "john_doe",
  "title": "Complete capstone project",
  "description": "Finish and submit the task management API",
  "due_date": "2025-10-25",
  "priority": "High",
  "status": "Completed",
  "completed_at": "2025-10-19T14:30:00Z",
  "created_at": "2025-10-19T10:30:00Z",
  "updated_at": "2025-10-19T14:30:00Z"
}
```

## 🔒 Security Features

- Password hashing using Django's built-in system
- Token-based authentication
- User-specific task access (users can only see their own tasks)
- Due date validation (must be in the future)
- Completed tasks cannot be edited unless marked incomplete

## 🧪 Testing

### Using Django Admin

1. Access admin panel: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage users and tasks through the interface

### Using API Browsable Interface

1. Navigate to `http://127.0.0.1:8000/api/tasks/`
2. Use the browsable API to test endpoints
3. Make sure to include authentication token in headers

### Using Postman or cURL

Import the API endpoints into Postman and test each endpoint with proper authentication headers.

## 📁 Project Structure
```
task_management_api/
├── task_api/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/                 # Tasks app
│   ├── models.py         # Task model
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin configuration
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚧 Known Issues & Future Improvements

### Current Limitations
- SQLite database (suitable for development only)
- No pagination for large task lists
- Basic error handling

### Future Enhancements
- Deploy to production (Heroku/Render/PythonAnywhere)
- Add task categories
- Implement recurring tasks
- Email notifications for due dates
- Task collaboration features
- Advanced search functionality

## 📝 Project Requirements Met

✅ User authentication (register, login, logout)  
✅ Task CRUD operations  
✅ Task attributes (title, description, due_date, priority, status)  
✅ Due date validation (must be in future)  
✅ Mark tasks complete/incomplete  
✅ Completed tasks cannot be edited (must be marked incomplete first)  
✅ Filter tasks by status, priority, due_date  
✅ Sort tasks by due_date or priority  
✅ User-specific task access (permissions)  
✅ RESTful API design  
✅ Proper HTTP methods and status codes  

## 👨‍💻 Author

**Jesse Ubani**
- GitHub: [@UbaniTheFirst](https://github.com/UbaniTheFirst)
- Project: ALX Backend Development Capstone

## 🙏 Acknowledgments

- ALX Africa for the opportunity and guidance
- Django and Django REST Framework documentation
- Fellow ALX learners for support and collaboration

---

**Built with ❤️ as part of ALX Backend Development Program - October 2025**
