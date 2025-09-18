"""
=========================================
STUDENTCONNECT DATABASE MODELS
=========================================

This module defines the database schema for the StudentConnect platform.
It includes user management, profile system, and event management models
with proper relationships and validation.

Database Schema:
1. User - Extended Django user model for authentication
2. UserProfile - Role-based profiles (Student/Organizer) 
3. Event - Event management with approval workflow

Key Features:
- Role-based user system (Students and Organizers)
- Event approval workflow with status tracking
- File upload handling for avatars and event flyers
- Proper foreign key relationships and constraints
- Comprehensive event categorization system
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    This model provides the foundation for authentication and user management.
    It includes all built-in Django user fields:
    - username: Unique identifier for login
    - email: User's email address
    - password: Hashed password for authentication
    - first_name/last_name: User's display name
    - is_active: Account activation status
    - date_joined: Registration timestamp
    
    Future extensions can be added here for platform-specific user data.
    """
    # Currently using default AbstractUser fields
    # Additional custom fields can be added here as needed
    pass


class UserProfile(models.Model):
    """
    User Profile model for role-based access control.
    
    This model extends the User model to support different user types
    (Students and Organizers) with role-specific functionality.
    Each user can have multiple profiles for different roles.
    
    Relationships:
    - One-to-Many with User (a user can have multiple role profiles)
    - One-to-Many with Event (organizers can create multiple events)
    
    Fields:
    - user_type: Determines platform permissions and interface
    - contact_number: Optional contact information
    - avatar: Profile picture for personalization
    """
    
    # User type choices for role-based access control
    USER_TYPES = (
        ("student", "Student"),       # Students browse and participate in events
        ("organizer", "Organizer"),   # Organizers create and manage events
    )

    # Relationships
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="profiles",
        help_text="The Django user this profile belongs to"
    )
    
    # Profile fields
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES,
        help_text="Role type determines platform permissions and interface"
    )
    contact_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Optional contact number for communication"
    )
    avatar = models.ImageField(
        upload_to="avatars/", 
        blank=True, 
        null=True,
        help_text="Profile picture uploaded to media/avatars/"
    )

    class Meta:
        # Prevent duplicate profiles - one user can only have one profile per type
        unique_together = ("user", "user_type")

    def __str__(self):
        """String representation showing username and role"""
        return f"{self.user.username} ({self.user_type})"


class Event(models.Model):
    """
    Event model for managing hackathons, workshops, internships, and tech events.
    
    This model handles the complete event lifecycle from creation through
    approval to publication. It includes a comprehensive approval workflow
    to ensure quality control of platform content.
    
    Relationships:
    - Many-to-One with UserProfile (organizer who created the event)
    
    Workflow:
    1. Organizer creates event (status: pending)
    2. Admin reviews and approves/denies event
    3. Approved events appear in student dashboard
    4. Denied events can be revised and resubmitted
    """
    
    # Event approval status for workflow management
    STATUS_CHOICES = (
        ("pending", "Pending"),     # Awaiting admin review
        ("approved", "Approved"),   # Approved and visible to students
        ("denied", "Denied"),       # Rejected with feedback
    )

    # Event categories for organization and filtering
    CATEGORY_CHOICES = (
        ("hackathon", "Hackathon"),     # Coding competitions and hackathons
        ("workshop", "Workshop"),       # Educational workshops and seminars
        ("internship", "Internship"),   # Internship opportunities
        ("techevent", "Tech Event"),    # General technology events
    )

    # Relationships
    organizer = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name="events",
        help_text="The organizer profile that created this event"
    )
    
    # Basic event information
    title = models.CharField(
        max_length=255,
        help_text="Event title displayed to students"
    )
    description = models.TextField(
        help_text="Detailed event description with objectives and requirements"
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default="techevent",
        help_text="Event category for filtering and organization"
    )
    
    # Event scheduling
    date = models.DateField(
        help_text="Event date (YYYY-MM-DD format)"
    )
    time = models.TimeField(
        help_text="Event start time (HH:MM format)"
    )
    location = models.CharField(
        max_length=255,
        help_text="Event venue or online platform details"
    )
    
    # Visual content
    event_flyer = models.ImageField(
        upload_to="event_flyers/", 
        blank=True, 
        null=True, 
        help_text="Upload event flyer/poster for visual appeal"
    )
    
    # Additional event information
    event_link = models.URLField(blank=False, null=False, help_text="Registration or event website link (Required)")
    additional_details = models.TextField(blank=True, null=True, help_text="Additional information about the event")
    contact_email = models.EmailField(blank=True, null=True, help_text="Contact email for event inquiries")
    requirements = models.TextField(blank=True, null=True, help_text="Prerequisites or requirements for participants")
    prizes = models.TextField(blank=True, null=True, help_text="Prizes or benefits for participants")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    denial_reason = models.TextField(blank=True, null=True)
    
    # Deletion tracking (soft delete)
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="When the event was deleted by admin")
    deleted_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='deleted_events', help_text="Admin who deleted the event")
    
    # Auto-styling fields added when event is approved
    featured_image = models.URLField(blank=True, null=True, help_text="Auto-assigned based on category")
    color_theme = models.CharField(max_length=20, blank=True, null=True, help_text="Auto-assigned color theme")
    styling_applied = models.BooleanField(default=False, help_text="Whether auto-styling has been applied")
    is_featured = models.BooleanField(default=False, help_text="Featured events get special styling")

    def __str__(self):
        return self.title
    
    @property
    def is_deleted(self):
        """Check if event is soft deleted"""
        return self.deleted_at is not None
    
    def soft_delete(self, deleted_by_user):
        """Soft delete the event"""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by_user
        self.save()

    def apply_auto_styling(self):
        """Automatically apply styling when event is approved"""
        if self.styling_applied:
            return  # Already styled
            
        # Category-based images and colors
        styling_config = {
            'hackathon': {
                'images': [
                    'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400',
                    'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=400',
                    'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=400'
                ],
                'color': '#e74c3c',  # Red
            },
            'workshop': {
                'images': [
                    'https://images.unsplash.com/photo-1620712943543-2fd617224887?w=400',
                    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400',
                    'https://images.unsplash.com/photo-1517180102446-f3ece451e9d8?w=400'
                ],
                'color': '#3498db',  # Blue
            },
            'internship': {
                'images': [
                    'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=400',
                    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
                    'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=400'
                ],
                'color': '#2ecc71',  # Green
            },
            'techevent': {
                'images': [
                    'https://images.unsplash.com/photo-1587825140708-df876c12b44e?w=400',
                    'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400',
                    'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400'
                ],
                'color': '#9b59b6',  # Purple
            }
        }
        
        import random
        config = styling_config.get(self.category, styling_config['techevent'])
        
        # Only assign random image if organizer didn't upload a flyer
        if not self.event_flyer:
            self.featured_image = random.choice(config['images'])
        else:
            # Use the uploaded flyer as the featured image
            # Use the proper Django URL method for uploaded files
            self.featured_image = self.event_flyer.url
            
        self.color_theme = config['color']
        self.styling_applied = True
        
        # Mark as featured if it's recent or special categories
        from datetime import date, timedelta
        if self.date >= date.today() - timedelta(days=7):
            self.is_featured = True
            
        self.save()
