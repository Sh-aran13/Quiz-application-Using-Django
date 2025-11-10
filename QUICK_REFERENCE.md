# Quick Reference Guide

## 🚀 Quick Start Commands

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Update database password
# Edit quiz_project/settings.py line 76-82

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

### Or use batch files (Windows):
```bash
setup.bat   # First time setup
run.bat     # Start server
```

## 🔗 Important URLs

- **Home/Login**: http://127.0.0.1:8000/
- **Register**: http://127.0.0.1:8000/register/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/
- **Student Dashboard**: http://127.0.0.1:8000/student-dashboard/
- **Profile**: http://127.0.0.1:8000/profile/
- **Django Admin**: http://127.0.0.1:8000/admin/

## 📋 Common Tasks

### Create Admin User
1. Go to: http://127.0.0.1:8000/register/
2. Select: Admin
3. Fill form and submit

### Create Student User
1. Go to: http://127.0.0.1:8000/register/
2. Select: Student
3. Fill form (including roll number and branch)
4. Submit

### Create a Quiz
1. Login as Admin
2. Click "Create New Quiz"
3. Enter title, description, time limit
4. Click "Create Quiz"
5. Add questions on next page

### Take a Quiz
1. Login as Student
2. Find quiz in "Available Quizzes"
3. Click "Take Test"
4. Answer questions
5. Navigate using Next/Previous
6. Click Submit when done

### Export Results
1. Login as Admin
2. Click "View Results"
3. Select a quiz from dropdown
4. Click "Download Excel" or "Download PDF"

## 🗄️ Database Configuration

Location: `quiz_project/settings.py` (lines 76-82)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password_here',  # CHANGE THIS
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔐 Default Setup

### Database
- **Name**: quiz_db
- **User**: postgres
- **Password**: (set your own)
- **Host**: localhost
- **Port**: 5432

### Django
- **Debug**: True (development)
- **Secret Key**: Generated
- **Allowed Hosts**: localhost, 127.0.0.1

## 📁 Important Files

### Configuration
- `quiz_project/settings.py` - Main settings
- `quiz_project/urls.py` - URL routing
- `requirements.txt` - Dependencies

### Application
- `quiz/models.py` - Database models
- `quiz/views.py` - Business logic
- `quiz/forms.py` - Form definitions
- `quiz/urls.py` - App URLs

### Templates
- `templates/quiz/` - All HTML templates

## 🔧 Troubleshooting

### Can't connect to database
```bash
# Check PostgreSQL is running
# Verify database exists: quiz_db
# Update password in settings.py
```

### Migrations error
```bash
# Delete migration files (keep __init__.py)
python manage.py makemigrations
python manage.py migrate
```

### Port 8000 in use
```bash
# Use different port
python manage.py runserver 8080
```

### Module not found
```bash
# Install dependencies
pip install -r requirements.txt
```

## 📊 Model Relationships

```
User
├── Quiz (created_by)
│   ├── Question
│   └── QuizAttempt
│       └── StudentAnswer
```

## 🎯 User Roles

### Admin Can:
- Create quizzes
- Add/delete questions
- View all results
- Export results
- Access admin dashboard

### Student Can:
- View available quizzes
- Attempt each quiz once
- View their results
- Access student dashboard
- View profile

## ⚡ Keyboard Shortcuts

### During Quiz
- **Tab**: Move to next option
- **Enter**: Select option
- **Alt + N**: Next question (if button visible)

### General
- **Ctrl + C**: Stop server (in terminal)
- **F5**: Refresh page
- **Ctrl + Shift + R**: Hard refresh

## 🎨 Color Codes

- **Primary**: #667eea (Purple-blue)
- **Success**: #48bb78 (Green)
- **Danger**: #e53e3e (Red)
- **Secondary**: #718096 (Gray)
- **Warning**: Orange

## 📝 Form Validation

### Registration
- Username: Required, unique
- Email: Required, valid format
- Phone: Required
- Password: Required, min 8 characters
- Students: roll_number, branch required

### Quiz Creation
- Title: Required
- Description: Required
- Time Limit: Required, integer

### Question Creation
- Question Text: Required
- All Options: Required
- Correct Answer: Required (A/B/C/D)
- Marks: Required, positive integer

## 🔄 Workflow Summary

### Admin Workflow
```
Register → Login → Create Quiz → Add Questions → 
Wait for Attempts → View Results → Export
```

### Student Workflow
```
Register → Login → Browse Quizzes → Take Quiz → 
Submit → View Results → Check History
```

## 💡 Tips

1. **Password Security**: Use strong passwords
2. **Quiz Timer**: Pay attention to time limit
3. **One Attempt**: Choose answers carefully
4. **Navigation**: Use question navigator to jump
5. **Export**: Export results regularly for backup
6. **Profile**: Update profile info if needed

## 📞 Support Files

- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Detailed setup
- `PROJECT_SUMMARY.md` - Project overview
- `CHECKLIST.md` - Feature checklist
- `QUICK_REFERENCE.md` - This file

## 🎉 Ready to Start!

1. ✅ Setup PostgreSQL
2. ✅ Update settings.py
3. ✅ Run migrations
4. ✅ Create users
5. ✅ Start testing

**Visit**: http://127.0.0.1:8000/
