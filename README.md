
# 🧭 Messy Migration – Flask API Starter Kit

A fully working Flask-based API with JWT auth, CRUD, validation, tests, and database setup. Ideal for refactoring exercises, small projects, or backend interview assignments.

---

## 🚀 Quick Start (⏱️ ~5 Minutes)

### 📁 1. Clone the Project

```bash
git clone https://github.com/your-username/messy_migration.git
cd messy-migration
```

### 📦 2. Install Requirements

```bash
pip install -r requirements.txt
```

### ⚙️ 3. Add Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production
DATABASE_URL=sqlite:///users.db
FLASK_ENV=development
```

### 🛠️ 4. Initialize the Database

```bash
python init_db.py
```

> This creates `users.db` and inserts an admin user:  
> **Email**: `admin@example.com` | **Password**: `admin123`

### ▶️ 5. Run the Application

```bash
python app.py
```

> Access the API at: [http://localhost:5000](http://localhost:5000)

---

## 🔬 Test the API

### 🧪 Manual Testing

```bash
# Health Check
curl http://localhost:5000/

# Create User
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

### ✅ Run Automated Tests

```bash
pytest tests/ -v
```

---

## 🗂️ Project Structure

```
messy_migration/
├── app.py                   # Main application entry point
├── config.py                # Configuration management
├── init_db.py              # Database initialization script
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (create this)
├── users.db                # SQLite database (created after init_db.py)
├── app/                    # Main application package
│   ├── __init__.py         # Application factory
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── user.py         # User SQLAlchemy model
│   ├── routes/             # API endpoints (Blueprints)
│   │   ├── __init__.py
│   │   ├── users.py        # User CRUD operations
│   │   └── auth.py         # Authentication endpoints
│   ├── services/           # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py # User business operations
│   └── utils/              # Utilities and helpers
│       ├── __init__.py
│       ├── validators.py   # Input validation schemas
│       └── exceptions.py   # Custom exception classes
└── tests/                  # Test suite
    ├── __init__.py
    ├── conftest.py         # Test configuration
    └── test_users.py       # User API tests
```

---

## ❗ Troubleshooting

### ❌ Import Errors?
```bash
cd messy-migration
python app.py
```

### ❌ Database Errors?
```bash
rm users.db
python init_db.py
```

### ❌ Missing `__init__.py`?
```bash
find . -name "__init__.py"
```

### ❌ Missing Dependencies?
```bash
pip install -r requirements.txt
```

---

## 🧪 Security & Validation Tests

```bash
# SQL Injection (Should Fail)
curl "http://localhost:5000/user/1'; DROP TABLE users; --"

# Invalid Input (Should Return Validation Error)
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"invalid","password":"123"}'
```

---

## ⚡ Quick Command Reference

```bash
pip install -r requirements.txt  # Install deps
python init_db.py                # Create DB
python app.py                    # Run server
pytest tests/ -v                 # Run tests
```

---

## ✅ Success Checklist

- [x] Server runs on `python app.py`
- [x] Health check works
- [x] Users can register/login
- [x] Tests pass with `pytest`
- [x] `users.db` file exists
- [x] Admin login works: `admin@example.com / admin123`

---

## 📌 Next Steps

1. 🚀 Test all endpoints  
2. 🔐 Review security  
3. ⚠️ Check error handling  
4. 📝 Log changes in `CHANGES.md`  
5. ✅ Submit or deploy

