# 📘 Project Best Practices

## 1. Project Purpose
StudentConnect is a Django web application that facilitates event management for educational institutions. It provides role-based access for students and event organizers, with admin approval workflows for event creation. The platform supports user authentication, profile management, and event lifecycle management from creation to approval/denial.

## 2. Project Structure
```
studentconnect/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── studentconnect/              # Main project configuration
│   ├── settings.py              # Django settings and configuration
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py/asgi.py         # WSGI/ASGI application entry points
├── accounts/                    # Main application module
│   ├── models.py                # Database models (User, UserProfile, Event)
│   ├── views.py                 # View functions and business logic
│   ├── forms.py                 # Django forms for data validation
│   ├── urls.py                  # App-specific URL patterns
│   ├── admin.py                 # Django admin configuration
│   ├── signals.py               # Django signals for model events
│   ├── migrations/              # Database migration files
├── templates/                   # HTML templates (global)
│   ├── landing.html
│   ├── login.html
│   ├── student-dashboard.html
│   ├── organizer-dashboard.html
│   └── admin/                   # Admin-specific templates
├── static/                      # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
└── .venv/                       # Virtual environment
```

## 3. Test Strategy
- **Framework**: Django's built-in TestCase framework
- **Current State**: Minimal test coverage (empty tests.py files)
- **Recommended Approach**:
  - Unit tests for models, forms, and utility functions
  - Integration tests for views and user workflows
  - Test authentication and authorization logic
  - Test event approval/denial workflows
  - Use Django's test client for view testing

## 4. Code Style
- **Language**: Python 3.x with Django 5.2.6
- **Naming Conventions**:
  - Models: PascalCase (e.g., `UserProfile`, `Event`)
  - Functions/variables: snake_case (e.g., `login_view`, `user_type`)
  - URLs: kebab-case (e.g., `student-dashboard`, `create-event`)
  - Templates: kebab-case (e.g., `student-dashboard.html`)
- **Import Organization**: Django imports first, then local imports
- **Error Handling**: Use Django's messages framework for user feedback
- **Authentication**: Use Django's built-in authentication with custom User model

## 5. Common Patterns
- **Custom User Model**: Extends AbstractUser for future extensibility
- **Profile Pattern**: Separate UserProfile model with user_type field for role-based access
- **Status Workflow**: Events have pending/approved/denied status with admin approval
- **Form Validation**: Use Django ModelForms for data validation
- **Decorator Usage**: `@login_required` and `@user_passes_test` for access control
- **Get or Create Pattern**: Used for profile creation to avoid duplicates
- **Related Names**: Consistent use of related_name in ForeignKey relationships

## 6. Do's and Don'ts

### ✅ Do's
- Use Django's built-in authentication system
- Implement proper access control with decorators
- Use Django's messages framework for user feedback
- Follow Django's URL naming conventions
- Use ModelForms for form validation
- Implement proper model relationships with related_name
- Use unique_together constraints to prevent data duplication
- Organize templates in logical directories

### ❌ Don'ts
- Don't hardcode SECRET_KEY in production (currently in settings.py)
- Don't use DEBUG=True in production
- Don't bypass Django's CSRF protection
- Don't store sensitive data in version control
- Don't create duplicate user profiles (use get_or_create pattern)
- Don't forget to handle authentication edge cases
- Don't mix business logic in templates

## 7. Tools & Dependencies
- **Core Framework**: Django 5.2.6
- **Database**: SQLite3 (development), PostgreSQL recommended for production
- **Authentication**: Django's built-in auth system with custom User model
- **Forms**: Django Forms and ModelForms
- **Static Files**: Django's staticfiles app
- **Media Handling**: Django's media file handling for avatars
- **Admin Interface**: Django Admin with custom configurations

### Setup Instructions
1. Create virtual environment: `python -m venv .venv`
2. Activate virtual environment: `.venv\Scripts\activate` (Windows)
3. Install Django: `pip install django`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run development server: `python manage.py runserver`

## 8. Other Notes
- **Role-Based Access**: System supports dual roles (student/organizer) per user
- **Admin Workflow**: Events require admin approval before being visible
- **Profile Management**: Users can have multiple profiles with different roles
- **Media Files**: Avatar uploads are supported with proper file handling
- **Security Considerations**: 
  - Change SECRET_KEY for production
  - Set DEBUG=False in production
  - Configure ALLOWED_HOSTS properly
  - Use environment variables for sensitive settings
- **Database**: Currently uses SQLite for development; consider PostgreSQL for production
- **Future Enhancements**: Consider adding email notifications, event categories, and advanced search functionality