# StudentConnect 🎓

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive college event management platform that connects students and organizers, facilitating seamless event discovery, management, and participation.

## 🌟 Features

### For Students
- **User Registration & Authentication** - Secure account creation with role-based access
- **Event Discovery** - Browse and discover upcoming college events
- **Interactive Dashboard** - Real-time updates with auto-refresh functionality
- **Event Details** - Detailed event information with multimedia support
- **Profile Management** - Customizable user profiles with avatar uploads

### For Organizers
- **Event Creation & Management** - Create and manage events with rich details
- **Event Approval Workflow** - Submit events for administrative approval
- **Media Upload** - Upload event flyers and promotional materials
- **Event Categories** - Organize events by type (Academic, Cultural, Sports, etc.)
- **Contact Management** - Manage event contact information and links

### For Administrators
- **Event Approval System** - Review and approve/deny submitted events
- **User Management** - Manage student and organizer accounts
- **Platform Oversight** - Monitor platform activity and content

## 🛠️ Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Django's built-in authentication system
- **File Handling**: Django's file upload system
- **Security**: CSRF protection, secure session management

## 📦 Installation

### Prerequisites
- Python 3.13 or higher
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bhoumik-006/collage_project.git
   cd collage_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django==5.2.5
   pip install pillow  # For image handling
   ```

4. **Navigate to project directory**
   ```bash
   cd studentconnect
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`

## 🚀 Usage

### Getting Started

1. **Landing Page** - Visit the homepage to learn about the platform
2. **Registration** - Sign up as either a Student or Organizer
3. **Login** - Access your role-specific dashboard
4. **Explore Features** - Create events (Organizers) or browse events (Students)

### User Roles

#### Students
- Register with student credentials
- Access student dashboard with event listings
- View detailed event information
- Manage personal profile

#### Organizers
- Register with organizer credentials
- Create and submit events for approval
- Manage event details and media
- Track event approval status

#### Administrators
- Access Django admin panel
- Review and approve/deny events
- Manage user accounts and permissions

## 📁 Project Structure

```
studentconnect/
├── accounts/                 # User management and authentication
│   ├── models.py            # User, UserProfile, Event models
│   ├── views.py             # Authentication and dashboard logic
│   ├── forms.py             # User registration and profile forms
│   ├── urls.py              # URL routing
│   └── migrations/          # Database migration files
├── studentconnect/          # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/               # HTML templates
│   ├── landing.html         # Homepage
│   ├── login.html           # Login page
│   ├── student-dashboard.html   # Student interface
│   ├── organizer-dashboard.html # Organizer interface
│   └── event_detail.html    # Event details page
├── static/                  # Static files (CSS, JS, images)
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── admin/               # Admin static files
├── media/                   # User uploaded files
│   ├── avatars/             # Profile pictures
│   └── event_flyers/        # Event promotional images
├── manage.py                # Django management script
└── db.sqlite3               # Development database
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production deployment:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

### Security Features
- CSRF protection enabled
- Secure session management
- User input validation
- File upload security
- XSS protection

## 🎨 Features in Detail

### Authentication System
- Role-based registration (Student/Organizer)
- Secure login/logout functionality
- Profile management with avatar uploads
- Session-based authentication

### Event Management
- **Event Creation**: Rich event details with categories
- **Media Support**: Upload event flyers and images
- **Approval Workflow**: Administrative review process
- **Event Discovery**: Student-friendly event browsing

### Dashboard Interfaces
- **Real-time Updates**: Auto-refresh functionality
- **Responsive Design**: Mobile-friendly interfaces
- **Interactive Elements**: Modern UI components
- **Role-specific Content**: Tailored user experiences

## 🔮 Future Enhancements

- [ ] Event booking and ticket management
- [ ] Email notifications for event updates
- [ ] Social media integration
- [ ] Mobile application
- [ ] Advanced search and filtering
- [ ] Event analytics and reporting
- [ ] Chat system for event discussions
- [ ] Calendar integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Bhoumik** - *Initial work* - [Bhoumik-006](https://github.com/Bhoumik-006)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Contributors and testers
- College administration for project support

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team

---

**Made with ❤️ for college communities**
