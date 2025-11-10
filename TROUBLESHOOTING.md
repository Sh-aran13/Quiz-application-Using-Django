# Troubleshooting Guide

## Common Issues and Solutions

### 1. Database Connection Issues

#### Error: "password authentication failed for user 'postgres'"

**Solution:**
1. Open `quiz_project/settings.py`
2. Go to line 76 (DATABASES section)
3. Update the PASSWORD field with your PostgreSQL password:
```python
'PASSWORD': 'your_actual_password',
```

#### Error: "database 'quiz_db' does not exist"

**Solution:**
1. Open PostgreSQL (pgAdmin or psql)
2. Create database:
   - **Using pgAdmin**: Right-click Databases → Create → Database → Name: `quiz_db`
   - **Using psql**: Run `CREATE DATABASE quiz_db;`

#### Error: "could not connect to server"

**Solution:**
1. Check if PostgreSQL service is running:
   - Windows: Services → PostgreSQL → Start
   - Or restart your computer
2. Verify PostgreSQL is installed correctly

### 2. Migration Issues

#### Error: "No changes detected"

**Solution:**
```bash
# Force create migrations
python manage.py makemigrations quiz
python manage.py migrate
```

#### Error: "table already exists"

**Solution:**
```bash
# Fake the migrations
python manage.py migrate --fake
```

#### Error: "Migration failed"

**Solution:**
1. Delete all files in `quiz/migrations/` EXCEPT `__init__.py`
2. Drop the database and recreate it:
```sql
DROP DATABASE quiz_db;
CREATE DATABASE quiz_db;
```
3. Run migrations again:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Django Issues

#### Error: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
pip install -r requirements.txt
```

#### Error: "That port is already in use"

**Solution:**
```bash
# Use a different port
python manage.py runserver 8080

# Or find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

#### Error: "SECRET_KEY not set"

**Solution:**
The SECRET_KEY is already set in `settings.py`. If you see this error, check that the file hasn't been corrupted.

### 4. Template Issues

#### Error: "TemplateDoesNotExist"

**Solution:**
1. Check that `templates/quiz/` directory exists
2. Verify the template file name matches exactly
3. Check `settings.py` TEMPLATES configuration:
```python
'DIRS': [BASE_DIR / 'templates'],
```

### 5. Static Files Issues

#### Error: "Static files not loading"

**Solution:**
1. Create static directories if missing:
```bash
mkdir static
mkdir static\css
mkdir static\js
```

2. Collect static files:
```bash
python manage.py collectstatic
```

### 6. Authentication Issues

#### Error: "Captcha validation failed"

**Solution:**
- The captcha is case-sensitive
- Make sure to copy the exact numbers shown
- If captcha doesn't appear, refresh the page

#### Error: "Cannot login after registration"

**Solution:**
1. Check password meets requirements (min 8 characters)
2. Verify username doesn't contain special characters
3. Try registering again with a different username

### 7. Quiz Taking Issues

#### Error: "You have already attempted this quiz"

**Solution:**
This is by design - students can only attempt each quiz once. To reset:
1. Login to Django admin (create superuser first)
2. Delete the QuizAttempt record for that student-quiz combination

#### Error: "Timer doesn't start"

**Solution:**
1. Enable JavaScript in your browser
2. Clear browser cache
3. Try a different browser

#### Error: "Cannot submit quiz"

**Solution:**
1. Make sure all questions are answered
2. Check browser console for JavaScript errors (F12)
3. Try clicking Submit again

### 8. Admin Issues

#### Error: "Cannot create quiz"

**Solution:**
1. Ensure you're logged in as admin
2. Check that you filled all required fields
3. Verify time_limit is a number

#### Error: "Cannot add questions"

**Solution:**
1. Make sure the quiz was created successfully
2. All fields are required - fill them all
3. Correct answer must be A, B, C, or D

### 9. Export Issues

#### Error: "Excel export fails"

**Solution:**
```bash
pip install openpyxl
```

#### Error: "PDF export fails"

**Solution:**
```bash
pip install reportlab
```

#### Error: "File downloads but is empty"

**Solution:**
- Make sure there are quiz attempts to export
- Check that students have completed the quiz (not just started)

### 10. Installation Issues

#### Error: "pip: command not found"

**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# Or install pip
python -m ensurepip --upgrade
```

#### Error: "Python version error"

**Solution:**
- This project requires Python 3.8 or higher
- Check version: `python --version`
- Update Python if needed

### 11. Performance Issues

#### Issue: "Page loads slowly"

**Solution:**
1. Check database indexes are created (migrations should handle this)
2. Restart the server
3. Clear browser cache

#### Issue: "Timer is inaccurate"

**Solution:**
- This is normal for client-side timers
- The timer is for guidance only
- Actual quiz time is tracked server-side

### 12. Browser Issues

#### Issue: "Styles not applying"

**Solution:**
1. Hard refresh: `Ctrl + Shift + R`
2. Clear browser cache
3. Try incognito/private mode
4. Try a different browser (Chrome, Firefox, Edge)

#### Issue: "JavaScript not working"

**Solution:**
1. Enable JavaScript in browser settings
2. Disable browser extensions that might block scripts
3. Check browser console for errors (F12)

## Quick Fixes

### Reset Everything
```bash
# 1. Delete database
DROP DATABASE quiz_db;
CREATE DATABASE quiz_db;

# 2. Delete migrations
# Delete all files in quiz/migrations/ except __init__.py

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Restart server
python manage.py runserver
```

### Create Superuser (for Django admin)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Clear Sessions
```bash
python manage.py clearsessions
```

### Check for Errors
```bash
python manage.py check
```

## Debugging Tips

### Enable Debug Mode
In `settings.py`, ensure:
```python
DEBUG = True
```

### View Detailed Errors
When an error occurs:
1. Check the terminal where server is running
2. Check browser console (F12 → Console)
3. Check browser network tab (F12 → Network)

### Database Issues
1. Check PostgreSQL logs
2. Test connection with pgAdmin
3. Verify credentials in settings.py

### Template Issues
1. Check template file exists
2. Verify template name matches in view
3. Check for typos in template tags

## Common Mistakes

1. ❌ Forgetting to update database password
   ✅ Update in `settings.py` line 79

2. ❌ Not creating the database
   ✅ Create `quiz_db` in PostgreSQL

3. ❌ Not installing dependencies
   ✅ Run `pip install -r requirements.txt`

4. ❌ Not running migrations
   ✅ Run `python manage.py migrate`

5. ❌ Using wrong URL
   ✅ Use `http://127.0.0.1:8000/` not `localhost:8000`

6. ❌ Entering wrong captcha
   ✅ Copy exact numbers shown

7. ❌ Trying to attempt quiz twice
   ✅ This is intentional - one attempt only

8. ❌ Not filling all form fields
   ✅ All fields are required

## Getting Help

### Check These First:
1. ✅ PostgreSQL is running
2. ✅ Database `quiz_db` exists
3. ✅ Password in settings.py is correct
4. ✅ All dependencies installed
5. ✅ Migrations completed
6. ✅ Server is running
7. ✅ Using correct URL

### Log Files to Check:
- Django errors: Terminal where server runs
- Browser errors: F12 → Console
- Database errors: PostgreSQL logs

### If Still Stuck:
1. Read the error message carefully
2. Search error message online
3. Check Django documentation
4. Verify all setup steps completed
5. Try on a different browser
6. Restart everything (server, database, browser)

## System Requirements

### Minimum:
- Windows 7 or higher
- Python 3.8+
- PostgreSQL 12+
- 2GB RAM
- Modern web browser

### Recommended:
- Windows 10/11
- Python 3.10+
- PostgreSQL 14+
- 4GB RAM
- Chrome/Firefox latest version

## Emergency Reset

If nothing works:
```bash
# 1. Uninstall all packages
pip uninstall -r requirements.txt -y

# 2. Delete database
DROP DATABASE quiz_db;
CREATE DATABASE quiz_db;

# 3. Delete all Python cache
# Delete all __pycache__ folders
# Delete quiz/migrations/ files (except __init__.py)

# 4. Reinstall
pip install -r requirements.txt

# 5. Fresh start
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Contact & Support

For issues not covered here:
1. Check README.md
2. Check SETUP_GUIDE.md
3. Review code comments
4. Django documentation: https://docs.djangoproject.com/
5. PostgreSQL documentation: https://www.postgresql.org/docs/

---

**Remember**: Most issues are due to:
- ❌ Database not configured
- ❌ Migrations not run
- ❌ Dependencies not installed
- ❌ Typos in configuration

Double-check these first! 🔍
