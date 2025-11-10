# Quiz Application Setup Guide

## Quick Setup Instructions

### Step 1: Install PostgreSQL

1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Install PostgreSQL with default settings
3. Remember the password you set for the 'postgres' user during installation

### Step 2: Create Database

#### Option A: Using pgAdmin (GUI)
1. Open pgAdmin 4
2. Right-click on "Databases" → "Create" → "Database"
3. Enter database name: `quiz_db`
4. Click "Save"

#### Option B: Using Command Line
1. Open Command Prompt as Administrator
2. Navigate to PostgreSQL bin directory (usually: `C:\Program Files\PostgreSQL\<version>\bin`)
3. Run: `psql -U postgres`
4. Enter your PostgreSQL password
5. Execute: `CREATE DATABASE quiz_db;`
6. Type `\q` to exit

### Step 3: Update Database Configuration

Open `quiz_project/settings.py` and update the DATABASES section with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'postgres',              # Your PostgreSQL username
        'PASSWORD': 'your_password',      # Your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Start the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Common Issues and Solutions

### Issue 1: Password Authentication Failed
**Error**: `password authentication failed for user "postgres"`

**Solution**: 
- Update the PASSWORD in `settings.py` with your actual PostgreSQL password
- Make sure PostgreSQL service is running

### Issue 2: Database Does Not Exist
**Error**: `database "quiz_db" does not exist`

**Solution**:
- Create the database using pgAdmin or psql command line
- Make sure the database name in settings.py matches

### Issue 3: Port Already in Use
**Error**: `That port is already in use`

**Solution**:
- Use a different port: `python manage.py runserver 8080`
- Or stop the process using port 8000

### Issue 4: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
- Install dependencies: `pip install -r requirements.txt`
- Verify you're in the correct directory

## First Time Usage

### Create an Admin Account

1. Go to: http://127.0.0.1:8000/register/
2. Select Role: "Admin"
3. Fill in:
   - Username: admin
   - Email: admin@example.com
   - Phone: 1234567890
   - Password: (choose a strong password)
4. Click Register

### Create a Student Account

1. Go to: http://127.0.0.1:8000/register/
2. Select Role: "Student"
3. Fill in:
   - Username: student1
   - Email: student1@example.com
   - Phone: 9876543210
   - Roll Number: 2024001
   - Branch: Computer Science
   - Password: (choose a password)
4. Click Register

### Login

1. Go to: http://127.0.0.1:8000/
2. Enter username and password
3. Enter the captcha code shown on screen
4. Click Login

## Features to Test

### As Admin:
1. ✅ Create a new quiz
2. ✅ Add questions to the quiz
3. ✅ View quiz list on dashboard
4. ✅ View results after students attempt
5. ✅ Export results as Excel
6. ✅ Export results as PDF

### As Student:
1. ✅ View available quizzes
2. ✅ Attempt a quiz
3. ✅ Navigate between questions
4. ✅ See timer countdown
5. ✅ Submit quiz
6. ✅ View results
7. ✅ Check quiz history
8. ✅ View profile

## Directory Structure

```
f:\quiz\
├── manage.py
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md (this file)
├── quiz_project\
│   ├── settings.py (UPDATE DATABASE PASSWORD HERE)
│   ├── urls.py
│   └── wsgi.py
├── quiz\
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
└── templates\
    └── quiz\
        ├── base.html
        ├── login.html
        ├── register.html
        └── ... (other templates)
```

## Need Help?

If you encounter any issues:
1. Check that PostgreSQL is running
2. Verify database credentials in settings.py
3. Ensure all dependencies are installed
4. Check Python version (3.8+)
5. Make sure you're in the project directory

## Important Notes

- **Default Database Password**: The code has 'postgres' as the default password. CHANGE IT in settings.py!
- **One Attempt Only**: Students can only attempt each quiz once
- **Captcha Changes**: The captcha refreshes on each page load
- **Timer**: Quizzes are timed - submission is automatic when time runs out
- **Password Security**: All passwords are hashed and stored securely
