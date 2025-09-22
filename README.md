# StudentConnect 🎓

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> A comprehensive college event management platform that connects students and organizers, facilitating seamless event discovery, management, and participation with a unified account system.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🌟 Overview

StudentConnect is a modern, responsive web application designed to bridge the gap between students and event organizers in college environments. The platform features a **unified account system** that allows users to seamlessly switch between student and organizer roles, making event management and participation more intuitive than ever.

### Key Highlights
- **Unified Account System**: One account for both student and organizer functionalities
- **Role-based Dashboards**: Tailored interfaces for different user types
- **Real-time Updates**: Auto-refresh functionality for live event updates
- **Modern UI/UX**: Professional, responsive design across all devices
- **Comprehensive Event Management**: From creation to approval to participation

## 🚀 Features

### 🎓 For Students
- **Unified Account Access**: Single login for all platform features
- **Event Discovery Hub**: Browse upcoming events with advanced filtering
- **Interactive Dashboard**: Real-time event updates and notifications
- **Detailed Event Views**: Rich event information with multimedia support
- **Profile Management**: Customizable profiles with avatar uploads
- **Role Switching**: Seamlessly switch to organizer mode when needed

### 🎯 For Organizers
- **Event Creation Suite**: Comprehensive event creation with rich details
- **Media Management**: Upload event flyers and promotional materials
- **Approval Workflow**: Professional event submission and tracking system
- **Category Management**: Organize events by type (Hackathons, Workshops, etc.)
- **Contact Management**: Integrated contact and registration link management
- **Analytics Dashboard**: Track event performance and engagement

### 👨‍💼 For Administrators
- **Event Approval System**: Professional review and approval workflow
- **User Management**: Comprehensive user account management
- **Platform Analytics**: Monitor platform activity and usage metrics
- **Content Moderation**: Ensure quality and appropriate content
- **Database Management**: Advanced admin interface for all operations

### ⚡ Technical Features
- **Responsive Design**: Mobile-first approach with desktop optimization
- **Security First**: CSRF protection, secure sessions, input validation
- **File Management**: Secure image uploads with proper validation
- **Database Optimization**: Efficient queries and proper indexing
- **Error Handling**: Comprehensive error handling and user feedback

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.5
- **Language**: Python 3.13+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django's built-in auth system with custom profiles

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome for consistent iconography
- **Fonts**: Inter font family for professional typography

### Security & Performance
- **Security**: CSRF tokens, secure headers, input sanitization
- **Performance**: Optimized queries, static file compression
- **Validation**: Both client-side and server-side validation
- **Error Handling**: Comprehensive logging and error reporting

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.13 or higher** ([Download here](https://www.python.org/downloads/))
- **Git** ([Download here](https://git-scm.com/downloads))
- **pip** (Python package installer - comes with Python)

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB (8GB recommended for development)
- **Storage**: At least 500MB free space
- **Browser**: Chrome 80+, Firefox 75+, Safari 13+, or Edge 80+

### Development Tools (Recommended)
- **Code Editor**: Visual Studio Code, PyCharm, or Sublime Text
- **Database Client**: DB Browser for SQLite or pgAdmin for PostgreSQL
- **Git Client**: GitHub Desktop or command line Git

## 🔧 Installation

Follow these step-by-step instructions to set up StudentConnect on your local machine:

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Bhoumik-006/collage_project_final_.git

# Navigate to the project directory
cd collage_project_final_
```

### 2. Set Up Python Virtual Environment

```bash
# Create a virtual environment
python -m venv studentconnect_env

# Activate the virtual environment
# On Windows:
studentconnect_env\Scripts\activate
# On macOS/Linux:
source studentconnect_env/bin/activate
```

### 3. Install Dependencies

```bash
# Upgrade pip to the latest version
python -m pip install --upgrade pip

# Install Django
pip install django==5.2.5

# Install Pillow for image handling
pip install pillow

# Install additional recommended packages
pip install python-decouple  # For environment variables
pip install django-crispy-forms  # For better form styling (optional)
```

### 4. Navigate to Project Directory

```bash
# Navigate to the Django project folder
cd "final collage project/final collage project/final collage project/final collage project/Full Minor project/Full Minor project/studentconnect"
```

### 5. Configure the Database

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate

# Migrate existing users to unified system (if applicable)
python manage.py migrate_to_unified_accounts
```

### 6. Create Superuser Account

```bash
# Create an admin account
python manage.py createsuperuser

# Follow the prompts to set username, email, and password
```

### 7. Start the Development Server

```bash
# Run the development server
python manage.py runserver

# The server will start at http://127.0.0.1:8000/
```

### 8. Access the Application

Open your web browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## ⚙️ Configuration

### Environment Variables

For production deployment, create a `.env` file in the project root:

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=False

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/studentconnect

# Email settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Media and Static files
MEDIA_URL=/media/
STATIC_URL=/static/
```

### Database Configuration

#### For Development (SQLite - Default)
No additional configuration needed. The SQLite database will be created automatically.

#### For Production (PostgreSQL)
```python
# In settings.py, update DATABASES setting:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'studentconnect',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📖 Usage

### Getting Started

1. **Visit the Landing Page**
   - Navigate to http://127.0.0.1:8000/
   - Explore the platform features and information

2. **Create an Account**
   - Click "Sign Up" and choose your preferred initial role
   - Fill in your details (name, email, password)
   - The system creates both student and organizer profiles automatically

3. **Login and Explore**
   - Login with your credentials
   - Choose your role (Student or Organizer)
   - Explore the role-specific dashboard

### User Workflows

#### As a Student
1. **Dashboard Access**: View approved events in your student dashboard
2. **Event Discovery**: Browse events by category, date, or search
3. **Event Details**: Click on events to view detailed information
4. **Profile Management**: Update your profile and upload an avatar
5. **Role Switching**: Use the role switcher to access organizer features

#### As an Organizer
1. **Event Creation**: Create new events with detailed information
2. **Media Upload**: Add event flyers and promotional images
3. **Event Management**: Edit, delete, or track your submitted events
4. **Approval Tracking**: Monitor the approval status of your events
5. **Role Switching**: Switch to student mode to view approved events

#### As an Administrator
1. **Admin Panel**: Access Django admin at /admin/
2. **Event Approval**: Review and approve/deny submitted events
3. **User Management**: Manage user accounts and permissions
4. **Content Moderation**: Monitor platform content for quality

### Role Switching

The unified account system allows seamless role switching:

1. **In Any Dashboard**: Click the role switcher dropdown (⚡ icon)
2. **Select Role**: Choose between Student and Organizer modes
3. **Instant Switch**: No re-login required, instant access to new role

## 📁 Project Structure

```
studentconnect/
├── 📁 accounts/                     # User management and authentication
│   ├── 📄 models.py                # User, UserProfile, Event models
│   ├── 📄 views.py                 # Authentication and dashboard logic
│   ├── 📄 forms.py                 # User registration and event forms
│   ├── 📄 urls.py                  # URL routing for accounts
│   ├── 📄 admin.py                 # Admin interface configuration
│   ├── 📄 signals.py               # User signal handlers
│   ├── 📁 migrations/              # Database migration files
│   ├── 📁 management/              # Custom management commands
│   │   └── 📁 commands/
│   │       └── 📄 migrate_to_unified_accounts.py
│   └── 📁 templatetags/            # Custom template tags
├── 📁 studentconnect/              # Main project configuration
│   ├── 📄 settings.py              # Django settings and configuration
│   ├── 📄 urls.py                  # Main URL configuration
│   ├── 📄 wsgi.py                  # WSGI configuration for deployment
│   └── 📄 asgi.py                  # ASGI configuration for async
├── 📁 templates/                   # HTML templates
│   ├── 📄 landing.html             # Homepage template
│   ├── 📄 login.html               # Login/registration page
│   ├── 📄 student-dashboard.html   # Student interface
│   ├── 📄 organizer-dashboard.html # Organizer interface
│   ├── 📄 event_detail.html        # Event details page
│   ├── 📄 about.html               # About page
│   └── 📁 admin/                   # Admin interface templates
├── 📁 static/                      # Static files (CSS, JS, images)
│   ├── 📁 css/                     # Stylesheets
│   │   ├── 📄 student.css          # Student dashboard styles
│   │   ├── 📄 organizer.css        # Organizer dashboard styles
│   │   └── 📄 landing.css          # Landing page styles
│   ├── 📁 js/                      # JavaScript files
│   │   ├── 📄 student.js           # Student functionality
│   │   ├── 📄 organizer.js         # Organizer functionality
│   │   └── 📄 common.js            # Shared JavaScript
│   ├── 📁 images/                  # Static images and assets
│   └── 📁 admin/                   # Django admin static files
├── 📁 media/                       # User uploaded files
│   ├── 📁 avatars/                 # User profile pictures
│   └── 📁 event_flyers/            # Event promotional images
├── 📄 manage.py                    # Django management script
├── 📄 db.sqlite3                   # Development database
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Project documentation
├── 📄 TODO.md                      # Development tasks and roadmap
└── 📄 UNIFIED_ACCOUNT_IMPLEMENTATION.md  # Unified system docs
```

## 🔌 API Documentation

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login/` | GET, POST | User login and authentication |
| `/logout/` | POST | User logout |
| `/signup/` | POST | New user registration |
| `/organizer-signup/` | GET, POST | Organizer-specific signup |

### Dashboard Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/student-dashboard/` | GET | Student dashboard view |
| `/organizer-dashboard/` | GET | Organizer dashboard view |
| `/profile/update/` | POST | Update user profile |

### Event Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/create-event/` | POST | Create new event |
| `/edit-event/<id>/` | GET, POST | Edit existing event |
| `/delete-event/<id>/` | POST | Delete event |
| `/event/<id>/` | GET | View event details |

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with verbose output
python manage.py test --verbosity=2

# Generate coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Types

- **Unit Tests**: Model and utility function testing
- **Integration Tests**: View and form testing
- **Authentication Tests**: Login/logout functionality
- **Database Tests**: Model relationships and queries

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up environment variables
- [ ] Configure production database (PostgreSQL)
- [ ] Set up static files serving
- [ ] Configure media files storage
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure email backend
- [ ] Set up logging and monitoring

### Deployment Options

#### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create studentconnect-app

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

#### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🎨 Customization

### Theming

The application supports easy theming through CSS custom properties:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #f59e0b;
    --accent-color: #10b981;
    --background-color: #f8fafc;
    --text-color: #0f172a;
}
```

### Adding New Event Categories

1. Update the `CATEGORY_CHOICES` in `models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update templates and forms as needed

### Custom User Fields

Add custom fields to the `UserProfile` model and create appropriate migrations.

## 🔧 Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check if port 8000 is in use
netstat -an | grep 8000

# Use different port
python manage.py runserver 8080
```

#### Database Issues
```bash
# Reset database (⚠️ Deletes all data)
rm db.sqlite3
python manage.py migrate

# Fix migration conflicts
python manage.py migrate --fake accounts zero
python manage.py migrate accounts
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_URL in settings.py
```

### Performance Optimization

- **Database**: Add indexes to frequently queried fields
- **Images**: Compress uploaded images automatically
- **Caching**: Implement Redis caching for frequently accessed data
- **CDN**: Use CDN for static file delivery in production

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/collage_project_final_.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guidelines
   - Add comments to complex code
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python manage.py test
   ```

5. **Commit and Push**
   ```bash
   git commit -m "Add amazing new feature"
   git push origin feature/amazing-new-feature
   ```

6. **Create Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include screenshots for UI changes

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Documentation**: Update README and inline docs
- **Testing**: Add tests for new features
- **Security**: Never commit sensitive information

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Bhoumik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👥 Authors & Contributors

### Core Team
- **Bhoumik** - *Project Lead & Full-Stack Developer* - [Bhoumik-006](https://github.com/Bhoumik-006)

### Contributors
- Thanks to all contributors who have helped improve this project
- Special thanks to the Django community for the excellent framework

## 🙏 Acknowledgments

- **Django Framework**: For providing a robust web development framework
- **Font Awesome**: For beautiful icons and UI elements
- **Unsplash**: For high-quality placeholder images
- **Inter Font**: For professional typography
- **College Community**: For feedback and testing support
- **Open Source Community**: For inspiration and best practices

## 📞 Support & Contact

### Getting Help

- **Documentation**: Check this README and inline documentation
- **Issues**: [Create a GitHub issue](https://github.com/Bhoumik-006/collage_project_final_/issues)
- **Discussions**: Use GitHub Discussions for questions and ideas

### Contact Information

- **Email**: [Contact via GitHub](https://github.com/Bhoumik-006)
- **GitHub**: [@Bhoumik-006](https://github.com/Bhoumik-006)
- **Project Repository**: [collage_project_final_](https://github.com/Bhoumik-006/collage_project_final_)

### Reporting Bugs

When reporting bugs, please include:
- Python and Django versions
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots (if applicable)

---

<div align="center">

**Made with ❤️ for college communities worldwide**

[![GitHub stars](https://img.shields.io/github/stars/Bhoumik-006/collage_project_final_.svg?style=social)](https://github.com/Bhoumik-006/collage_project_final_)
[![GitHub forks](https://img.shields.io/github/forks/Bhoumik-006/collage_project_final_.svg?style=social)](https://github.com/Bhoumik-006/collage_project_final_/fork)

*StudentConnect - Connecting students and organizers for better college experiences*

</div>
