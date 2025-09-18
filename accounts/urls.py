from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh-csrf/', views.refresh_csrf_token, name='refresh_csrf_token'),
    # LOGOUT URLS COMPLETELY REMOVED FOR SECURITY
    # path("logout/", views.logout_view, name="logout"),
    # path("secure-logout/", views.secure_logout, name="secure_logout"),
    path("session-destroy/", views.session_destroy, name="session_destroy"),
    path("enable-logout/", views.enable_logout, name="enable_logout"),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer-dashboard'),
    path('create-event/', views.create_event, name='create_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path("save-profile/", views.save_profile, name="save_profile"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/deny/', views.deny_event_view, name='deny_event'),
    # Removed debug/test routes to keep production clean
    path('organizer-signup/', views.organizer_signup, name='organizer_signup'),
]
    