# 📊 StudentConnect Database Management Guide

## 🗄️ Database Overview

Your StudentConnect project uses **SQLite** as the database engine with Django ORM for data management.

### Database Configuration
- **Engine**: SQLite3
- **Location**: `db.sqlite3` in project root
- **Models**: Custom User, UserProfile, Event
- **ORM**: Django ORM with migrations

---

## 🏗️ Database Structure

### 1. **User Model** (Custom AbstractUser)
```python
# Fields:
- id (Primary Key)
- username (Unique)
- email 
- password (Hashed)
- first_name
- last_name
- is_active
- date_joined
- is_staff
- is_superuser
```

### 2. **UserProfile Model** (Role Management)
```python
# Fields:
- id (Primary Key)
- user (ForeignKey to User)
- user_type ('student' or 'organizer')
- contact_number (Optional)
- avatar (ImageField)

# Unique Together: (user, user_type)
```

### 3. **Event Model** (Event Management)
```python
# Fields:
- id (Primary Key)
- organizer (ForeignKey to UserProfile)
- title
- description
- category ('hackathon', 'workshop', 'internship', 'techevent')
- date
- time
- location
- event_flyer (ImageField)
- event_link (Required URL)
- status ('pending', 'approved', 'denied')
- additional_details
- contact_email
- requirements
- prizes
- denial_reason
- deleted_at (Soft Delete)
- deleted_by (ForeignKey to User)
- featured_image (Auto-generated)
- color_theme (Auto-generated)
- styling_applied (Boolean)
- is_featured (Boolean)
```

---

## 🛠️ Database Management Commands

### Basic Database Operations

#### 1. **Check Database Status**
```bash
# Navigate to project directory
cd "d:\collage complete project\final collage project\final collage project\final collage project\final collage project\Full Minor project\Full Minor project\studentconnect"

# Check current migration status
python manage.py showmigrations

# Check database schema
python manage.py dbshell
```

#### 2. **Create and Apply Migrations**
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create migrations for specific app
python manage.py makemigrations accounts
```

#### 3. **Database Reset and Backup**
```bash
# ⚠️ BACKUP DATABASE FIRST
copy db.sqlite3 db_backup.sqlite3

# Reset database (DANGER: Deletes all data)
del db.sqlite3
python manage.py migrate

# Restore from backup
copy db_backup.sqlite3 db.sqlite3
```

### Data Management Commands

#### 4. **Create Superuser (Admin Access)**
```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

#### 5. **Django Shell (Interactive Database Access)**
```bash
# Open Django shell
python manage.py shell

# Sample shell commands:
from accounts.models import User, UserProfile, Event

# Count records
User.objects.count()
UserProfile.objects.count()
Event.objects.count()

# View recent events
Event.objects.order_by('-id')[:5]

# Filter by status
Event.objects.filter(status='approved')
```

---

## 📊 Database Inspection Tools

### 1. **Django Admin Panel**
```bash
# Start server
python manage.py runserver

# Access admin at: http://127.0.0.1:8000/admin/
# Login with superuser credentials
```

### 2. **SQLite Browser Commands**
```bash
# Open database directly
python manage.py dbshell

# Common SQL queries:
.tables                          # List all tables
.schema accounts_user           # Show table structure
SELECT COUNT(*) FROM accounts_user;
SELECT * FROM accounts_event WHERE status='pending';
```

### 3. **Model Inspection**
```python
# In Django shell (python manage.py shell)
from accounts.models import User, UserProfile, Event

# Get model fields
User._meta.get_fields()
Event._meta.get_fields()

# Check relationships
UserProfile._meta.get_field('user')
Event._meta.get_field('organizer')
```

---

## 🔧 Common Database Tasks

### User Management
```python
# In Django shell
from accounts.models import User, UserProfile

# Create user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create profiles
student_profile = UserProfile.objects.create(
    user=user,
    user_type='student'
)

organizer_profile = UserProfile.objects.create(
    user=user,
    user_type='organizer'
)

# Find users by type
students = UserProfile.objects.filter(user_type='student')
organizers = UserProfile.objects.filter(user_type='organizer')
```

### Event Management
```python
# In Django shell
from accounts.models import Event, UserProfile

# Get pending events
pending_events = Event.objects.filter(status='pending')

# Approve events
for event in pending_events:
    event.status = 'approved'
    event.apply_auto_styling()  # Auto-assign colors and images
    event.save()

# Get events by category
hackathons = Event.objects.filter(category='hackathon')
workshops = Event.objects.filter(category='workshop')
```

### Data Analysis
```python
# Event statistics
from django.db.models import Count
from accounts.models import Event, UserProfile

# Events by category
Event.objects.values('category').annotate(count=Count('id'))

# Events by status
Event.objects.values('status').annotate(count=Count('id'))

# Active organizers
UserProfile.objects.filter(
    user_type='organizer',
    events__isnull=False
).distinct().count()
```

---

## 🚨 Database Maintenance

### Regular Maintenance Tasks

#### 1. **Database Cleanup**
```python
# Remove soft-deleted events older than 30 days
from datetime import datetime, timedelta
from accounts.models import Event

old_deleted = Event.objects.filter(
    deleted_at__lt=datetime.now() - timedelta(days=30)
)
old_deleted.delete()  # Permanent deletion
```

#### 2. **Data Integrity Checks**
```python
# Check for orphaned profiles
UserProfile.objects.filter(user__isnull=True)

# Check for events without organizers
Event.objects.filter(organizer__isnull=True)

# Verify unique constraints
from django.db import IntegrityError
```

#### 3. **Performance Optimization**
```python
# Optimize queries with select_related
events_with_organizers = Event.objects.select_related(
    'organizer__user'
).filter(status='approved')

# Use prefetch_related for reverse relationships
users_with_profiles = User.objects.prefetch_related(
    'profiles'
).all()
```

---

## 📈 Database Monitoring

### Key Metrics to Track
1. **User Growth**: Total users, new registrations
2. **Event Activity**: Events created, approved, denied
3. **User Engagement**: Login frequency, profile completeness
4. **Data Quality**: Incomplete profiles, missing event details

### Monitoring Queries
```python
# Daily registration count
from django.utils import timezone
from datetime import timedelta

today = timezone.now().date()
new_users_today = User.objects.filter(
    date_joined__date=today
).count()

# Event approval rate
total_events = Event.objects.count()
approved_events = Event.objects.filter(status='approved').count()
approval_rate = (approved_events / total_events) * 100
```

---

## 🔒 Database Security

### Best Practices
1. **Regular Backups**: Copy `db.sqlite3` before major changes
2. **Access Control**: Use Django admin permissions carefully
3. **Data Validation**: Ensure proper model validation
4. **Audit Trail**: Track who makes changes to critical data

### Security Commands
```bash
# Check for security issues
python manage.py check --deploy

# Update dependencies
pip install --upgrade django

# Database integrity check
python manage.py check
```

---

## 🆘 Troubleshooting

### Common Issues

#### Migration Conflicts
```bash
# Reset migrations (DANGER: Data loss)
rm accounts/migrations/00*.py
python manage.py makemigrations accounts
python manage.py migrate
```

#### Database Corruption
```bash
# Check database integrity
python manage.py dbshell
PRAGMA integrity_check;

# Vacuum database (optimize)
VACUUM;
```

#### Performance Issues
```python
# Identify slow queries
import logging
logging.basicConfig(level=logging.DEBUG)

# Use database connection pooling for production
# Add django-debug-toolbar for query analysis
```

---

## 📝 Quick Reference

### Essential Commands
```bash
# Development workflow
python manage.py makemigrations    # Create migrations
python manage.py migrate          # Apply migrations
python manage.py runserver        # Start development server
python manage.py shell           # Interactive Python shell
python manage.py createsuperuser # Create admin user

# Database inspection
python manage.py showmigrations   # Show migration status
python manage.py dbshell         # SQLite command line
python manage.py check           # Check for issues
```

### Important File Locations
- **Database**: `db.sqlite3`
- **Models**: `accounts/models.py`
- **Migrations**: `accounts/migrations/`
- **Settings**: `studentconnect/settings.py`
- **Media Files**: `media/avatars/`, `media/event_flyers/`

Remember to always backup your database before making significant changes! 🛡️
