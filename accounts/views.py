"""
=========================================
STUDENTCONNECT VIEWS MODULE
=========================================

This module contains all Django views for the StudentConnect platform.
It handles user authentication, dashboard rendering, event management,
and administrative functions.

Key Functionality:
- User registration and authentication (students and organizers)
- Dashboard rendering with event data
- Event creation, editing, and approval workflow
- Admin interface for platform management
- CSRF token management for security
- Professional About page rendering

Security Features:
- CSRF protection on all forms
- User role-based access control
- Login required decorators
- Admin-only view restrictions
"""

# Django core imports for web functionality
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()  # Get the custom user model

# Security and permission imports
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse

# Local app imports
from .models import UserProfile, Event
from .forms import EventForm, DenyEventForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import secrets

def is_admin(user):
    """
    Helper function to check if user has administrator privileges.
    
    Args:
        user: Django User object
        
    Returns:
        bool: True if user is superuser (admin), False otherwise
    """
    return user.is_superuser


def landing(request):
    """
    Render the main landing page for StudentConnect.
    
    This view serves the homepage with hero section, features,
    and authentication options for both students and organizers.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        HttpResponse: Rendered landing.html template
    """
    return render(request, "landing.html")


def about(request):
    """
    Render the professional About page for StudentConnect platform.
    
    Displays information about the platform, mission, vision,
    key features, and company information.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        HttpResponse: Rendered about.html template
    """
    return render(request, "about.html")


@csrf_protect
def signup_view(request):
    """
    Handle user registration for both students and organizers.
    
    Processes POST requests to create new user accounts with
    appropriate user profiles based on user type selection.
    Includes password validation and error handling.
    
    Args:
        request: Django HttpRequest object containing form data
        
    Returns:
        HttpResponse: Redirect to dashboard on success, or form with errors
    """
    if request.method == "POST":
        # Extract form data from POST request
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user_type = request.POST.get("user_type")  # "student" or "organizer"

        # Handle empty or None values
        if not password or not confirm_password:
            messages.error(request, "Both password fields are required.")
            return render(request, "login.html", {
                'show_signup': True,
                'name': name,
                'email': email,
                'user_type': user_type,
                'password_error': True
            })

        # Password validation - ensure both passwords match
        # Strip whitespace to handle any trailing spaces
        password = password.strip()
        confirm_password = confirm_password.strip()
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please ensure both password fields are identical.")
            return render(request, "login.html", {
                'show_signup': True,
                'name': name,
                'email': email,
                'user_type': user_type,
                'password_mismatch': True
            })

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            existing_user = User.objects.get(username=email)
            # Check if they already have this user type
            if UserProfile.objects.filter(user=existing_user, user_type=user_type).exists():
                messages.error(request, f"An account with this email already exists as a {user_type}. Please log in instead.")
                return render(request, "login.html", {
                    'email': email,
                    'user_type': user_type
                })
            else:
                # User exists but with different user type
                messages.error(request, f"This email is already registered as a different user type. Please use a different email or log in with your existing account.")
                return render(request, "login.html", {
                    'show_signup': True,
                    'name': name,
                    'email': email,
                    'user_type': user_type
                })

        # Create new user
        try:
            user = User.objects.create_user(username=email, email=email, first_name=name, password=password)
            # Create the requested profile
            UserProfile.objects.create(user=user, user_type=user_type)
            # If signing up as student, also create organizer profile for dual role functionality
            if user_type == "student":
                UserProfile.objects.create(user=user, user_type="organizer")
                messages.success(request, "Account created successfully! Welcome to StudentConnect. You can now login as both Student and Organizer with this email.")
            else:
                messages.success(request, f"Account created successfully! Welcome to StudentConnect. Please log in with your new {user_type} account.")
            return render(request, "login.html", {
                'email': email,
                'user_type': user_type
            })
        except Exception as e:
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return render(request, "login.html", {
                'show_signup': True,
                'name': name,
                'email': email,
                'user_type': user_type
            })

    return redirect("login")

    return render(request, "login.html")




@csrf_protect
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        # Check if user exists
        try:
            user_exists = User.objects.get(username=email)
        except User.DoesNotExist:
            # User doesn't exist - show registration message
            messages.error(request, f"No account found with this email address. Please sign up to create a new account.")
            return render(request, "login.html", {
                'show_signup': True,
                'email': email,
                'user_type': user_type
            })

        # Try to authenticate
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if a profile exists for the requested user_type
            try:
                profile = UserProfile.objects.get(user=user, user_type=user_type)
                login(request, user)
                if profile.user_type == "student":
                    return redirect("student-dashboard")
                elif profile.user_type == "organizer":
                    return redirect("organizer-dashboard")
            except UserProfile.DoesNotExist:
                # Special case: If trying to login as organizer but have student profile, create organizer profile
                if user_type == "organizer":
                    try:
                        student_profile = UserProfile.objects.get(user=user, user_type="student")
                        # Create organizer profile for this user
                        UserProfile.objects.create(user=user, user_type="organizer")
                        login(request, user)
                        messages.success(request, "Welcome! Your organizer account has been created. You can now access organizer features.")
                        return redirect("organizer-dashboard")
                    except UserProfile.DoesNotExist:
                        pass  # Fall through to error message
                messages.error(request, f"You don't have a {user_type} account. You may have registered as a different user type. Please check your account type or sign up as a {user_type}.")
                return render(request, "login.html", {
                    'show_signup': True,
                    'email': email,
                    'user_type': user_type
                })
        else:
            # Wrong password or email
            messages.error(request, "Incorrect email or password. Please check your credentials and try again.")
            return render(request, "login.html", {
                'email': email,
                'user_type': user_type
            })

    # For GET requests, render the login page with fresh context
    response = render(request, "login.html")
    
    # Add cache-busting headers to ensure fresh CSRF tokens
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response



@login_required
def logout_view(request):
    """Simple, normal logout like any standard website"""
    if request.method == 'POST':
        username = request.user.username
        # Clear any custom session data
        request.session.flush()
        logout(request)
        return redirect('landing')
    
    # If GET request, redirect to dashboard
    return redirect('organizer-dashboard')


def enable_logout(request):
    """Enable logout for this session - called via AJAX when user confirms logout"""
    print(f"ENABLE_LOGOUT called: Method={request.method}, User={request.user.username if request.user.is_authenticated else 'Anonymous'}")
    
    if request.method == 'POST' and request.user.is_authenticated:
        # Add a small delay to prevent rapid-fire logout attempts
        import time
        time.sleep(0.1)  # Reduced delay
        
        # Check if enough time has passed since page load - reduced to 1 second
        last_page_load = request.session.get('last_page_load', 0)
        current_time = time.time()
        
        print(f"Time check: Current={current_time}, Last load={last_page_load}, Diff={current_time - last_page_load}")
        
        if current_time - last_page_load < 1:  # Reduced from 3 to 1 second
            print(f"TOO_SOON: Only {current_time - last_page_load} seconds since page load")
            return HttpResponse('TOO_SOON')
        
        # Enable logout with a timestamp
        request.session['logout_allowed'] = True
        request.session['logout_enabled_at'] = current_time
        print(f"LOGOUT ENABLED for user {request.user.username}")
        return HttpResponse('OK')
    
    print(f"ENABLE_LOGOUT FAILED: Method={request.method}, Auth={request.user.is_authenticated}")
    return HttpResponse('FAIL')


def secure_logout(request):
    """Completely secure logout endpoint that bypasses all middleware checks"""
    if (request.method == 'POST' and 
        request.user.is_authenticated and
        request.session.get('logout_allowed', False)):
        
        # Verify logout token
        logout_token = request.POST.get('logout_token')
        session_token = request.session.get('logout_token')
        
        if logout_token and session_token and logout_token == session_token:
            # Clear all session data before logout
            request.session.flush()
            logout(request)
            messages.success(request, 'You have been successfully logged out.')
            return redirect("landing")
    
    # If we get here, redirect back to dashboard
    messages.warning(request, 'Logout failed. Please try again.')
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user, user_type='organizer')
            return redirect('organizer-dashboard')
        except UserProfile.DoesNotExist:
            try:
                profile = UserProfile.objects.get(user=request.user, user_type='student')
                return redirect('student-dashboard')
            except UserProfile.DoesNotExist:
                return redirect('organizer-dashboard')
    return redirect("landing")


def session_destroy(request):
    """
    SIMPLIFIED: Direct logout with basic security checks
    """
    print(f"SESSION_DESTROY called: Method={request.method}, User={request.user.username if request.user.is_authenticated else 'Anonymous'}")
    
    if request.method == 'POST' and request.user.is_authenticated:
        
        # Basic verification steps
        logout_token = request.POST.get('logout_token')
        session_token = request.session.get('logout_token')
        confirmation = request.POST.get('confirm_logout')
        
        print(f"Tokens - POST: {logout_token[:10] if logout_token else None}..., Session: {session_token[:10] if session_token else None}...")
        print(f"Confirmation: {confirmation}")
        
        # Check basic security requirements
        if (logout_token and 
            session_token and 
            logout_token == session_token and
            confirmation == 'YES_LOGOUT_CONFIRMED'):
            
            print(f"AUTHORIZED LOGOUT: User {request.user.username} logging out via session-destroy")
            
            # Complete session destruction
            username = request.user.username
            
            # Log out and destroy session
            logout(request)
            request.session.flush()
            
            messages.success(request, f'User {username} has been successfully logged out.')
            return redirect("landing")
        else:
            print(f"FAILED LOGOUT ATTEMPT: User {request.user.username} - invalid tokens or confirmation")
            messages.error(request, 'Logout verification failed. Security tokens do not match.')
    else:
        print(f"INVALID REQUEST: Method={request.method}, Auth={request.user.is_authenticated}")
        messages.warning(request, 'Invalid logout request.')
    
    # Always redirect back to dashboard on failure
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user, user_type='organizer')
            return redirect('organizer-dashboard')
        except UserProfile.DoesNotExist:
            try:
                profile = UserProfile.objects.get(user=request.user, user_type='student')
                return redirect('student-dashboard')
            except UserProfile.DoesNotExist:
                return redirect('organizer-dashboard')
    return redirect("landing")


@ensure_csrf_cookie
def refresh_csrf_token(request):
    """Refresh CSRF token for AJAX requests"""
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'CSRF token refreshed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@ensure_csrf_cookie
def student_dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user , user_type="student")
    # Only show approved events to students that are not deleted
    approved_events = Event.objects.filter(status='approved', deleted_at__isnull=True).order_by('-date', '-time')
    
    return render(request, "student-dashboard.html", {
        "user": request.user,
        "profile": profile,
        "events": approved_events
    })


@login_required
@ensure_csrf_cookie
def organizer_dashboard(request):
    # Get the organizer profile, creating one only if it doesn't exist
    try:
        profile = UserProfile.objects.get(user=request.user, user_type="organizer")
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, user_type="organizer")
    
    # Refresh from database to ensure we have latest data
    profile.refresh_from_db()
    
    # Get active events for the organizer only
    active_events = Event.objects.filter(organizer=profile, deleted_at__isnull=True).order_by('-date', '-time')
    
    # Count by status for active events
    total_count = active_events.count()
    pending_count = active_events.filter(status='pending').count()
    approved_count = active_events.filter(status='approved').count()
    denied_count = active_events.filter(status='denied').count()
    
    return render(request, "organizer-dashboard.html", {
        "user": request.user,
        "profile": profile,
        "events": active_events,  # For backward compatibility
        "active_events": active_events,
        "total_count": total_count,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "denied_count": denied_count,
        "event_form": EventForm()
    })


@login_required
@csrf_protect
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Get the organizer profile for the current user
                organizer_profile = request.user.profiles.get(user_type='organizer')
                event = form.save(commit=False)
                event.organizer = organizer_profile
                # Save status from form cleaned data
                event.status = form.cleaned_data.get('status', 'pending')
                event.save()
                messages.success(request, 'Event created successfully!')
                return redirect('organizer-dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, 'You must have an organizer profile to create events.')
                return redirect('organizer-dashboard')
        else:
            messages.error(request, 'There was an error creating the event. Please check the form.')
    else:
        form = EventForm()
    
    # Make sure to pass form with errors to template
    return render(request, 'organizer-dashboard.html', {'form': form})

@login_required
@csrf_protect
def save_profile(request):
    if request.method == "POST":
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Save contact number
        contact_number = request.POST.get("contact_number")
        if contact_number:
            profile.contact_number = contact_number

        # Save avatar if uploaded
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]

        profile.save()
        messages.success(request, "Profile updated successfully!")

        # Redirect back to correct dashboard
        if profile.user_type == "student":
            return redirect("student-dashboard")
        elif profile.user_type == "organizer":
            return redirect("organizer-dashboard")

    return redirect("landing")

@user_passes_test(is_admin)
@csrf_protect
def deny_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = DenyEventForm(request.POST)
        if form.is_valid():
            event.status = 'denied'
            event.denial_reason = form.cleaned_data['denial_reason']
            event.save()
            messages.success(request, f'Event "{event.title}" has been denied.')
            return redirect('/admin/accounts/event/')
    else:
        form = DenyEventForm()

    return render(request, 'admin/deny_event.html', {'event': event, 'form': form})


@login_required
@csrf_protect
def edit_event(request, event_id):
    """Allow organizers to edit their own events"""
    # Get the organizer profile
    try:
        organizer_profile = request.user.profiles.get(user_type='organizer')
    except UserProfile.DoesNotExist:
        messages.error(request, 'You must be an organizer to edit events.')
        return redirect('organizer-dashboard')
    
    # Get the event and ensure it belongs to this organizer
    try:
        event = Event.objects.get(id=event_id, organizer=organizer_profile, deleted_at__isnull=True)
    except Event.DoesNotExist:
        # Check if event exists at all
        try:
            existing_event = Event.objects.get(id=event_id)
            if existing_event.deleted_at is not None:
                messages.error(request, 'This event has been deleted and cannot be edited.')
            else:
                messages.error(request, 'You can only edit your own events.')
        except Event.DoesNotExist:
            messages.error(request, 'Event not found.')
        return redirect('organizer-dashboard')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            # Save status from form cleaned data
            event.status = form.cleaned_data.get('status', event.status)
            event.save()
            messages.success(request, f'Event "{event.title}" has been updated successfully!')
            return redirect('organizer-dashboard')
        else:
            messages.error(request, 'There was an error updating the event. Please check the form.')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'edit-event.html', {
        'form': form,
        'event': event,
        'user': request.user,
        'profile': organizer_profile
    })


@login_required
def delete_event(request, event_id):
    """Allow organizers to delete their own events"""
    # Get the organizer profile
    try:
        organizer_profile = request.user.profiles.get(user_type='organizer')
    except UserProfile.DoesNotExist:
        messages.error(request, 'You must be an organizer to delete events.')
        return redirect('organizer-dashboard')
    
    # Get the event and ensure it belongs to this organizer
    event = get_object_or_404(Event, id=event_id, organizer=organizer_profile, deleted_at__isnull=True)
    
    if request.method == 'POST':
        event_title = event.title
        # Soft delete by the organizer themselves
        event.soft_delete(deleted_by_user=request.user)
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        return redirect('organizer-dashboard')
    
    return render(request, 'confirm-delete-event.html', {
        'event': event,
        'user': request.user,
        'profile': organizer_profile
    })


def event_detail(request, event_id):
    """Display detailed information about a specific event"""
    event = get_object_or_404(Event, id=event_id, status='approved')
    
    context = {
        'event': event,
    }
    
    return render(request, 'event_detail.html', context)


@login_required
@csrf_protect
def update_profile(request):
    """Handle profile updates including avatar upload"""
    user = request.user
    
    # Try to get the user's organizer profile first
    try:
        profile = UserProfile.objects.get(user=user, user_type='organizer')
    except UserProfile.DoesNotExist:
        # If no organizer profile, try student profile
        try:
            profile = UserProfile.objects.get(user=user, user_type='student')
        except UserProfile.DoesNotExist:
            # Create organizer profile as default
            profile = UserProfile.objects.create(user=user, user_type='organizer')
    
    if request.method == 'POST':
        updated = False
        
        # Update contact number
        contact_number = request.POST.get('contact_number')
        if contact_number and contact_number != profile.contact_number:
            profile.contact_number = contact_number
            updated = True
        
        # Handle avatar upload
        if 'avatar' in request.FILES and request.FILES['avatar']:
            profile.avatar = request.FILES['avatar']
            updated = True
        
        if updated:
            profile.save()
            if 'avatar' in request.FILES:
                messages.success(request, 'Profile picture updated successfully!')
            else:
                messages.success(request, 'Profile updated successfully!')
        else:
            messages.info(request, 'No changes were made to your profile.')
        
        # Redirect based on user type
        if profile.user_type == 'organizer':
            return redirect('organizer-dashboard')
        else:
            return redirect('student-dashboard')
    
    # Redirect based on user type
    if profile.user_type == 'organizer':
        return redirect('organizer-dashboard')
    else:
        return redirect('student-dashboard')


def url_test(request):
    """Deprecated: simple URL test. Removed in production cleanup."""
    return redirect('about')


@csrf_protect
def organizer_signup(request):
    """
    Handle organizer registration with proper validation.
    
    Fields:
    - Organization Name (name)
    - Official Email Address (email)
    - Create Password (password)
    - Confirm Password (confirm_password)
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        user_type = 'organizer'
        
        # Validation
        if not all([name, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'organizer_signup.html', {
                'name': name,
                'email': email
            })
        
        # Password confirmation validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'organizer_signup.html', {
                'name': name,
                'email': email
            })
        
        # Password strength validation
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'organizer_signup.html', {
                'name': name,
                'email': email
            })
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'organizer_signup.html', {
                'name': name,
                'email': email
            })
        
        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=name,
                password=password
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type
            )
            
            messages.success(request, 'Organizer account created successfully! You can now login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'organizer_signup.html', {
                'name': name,
                'email': email
            })
    
    return render(request, 'organizer_signup.html')


