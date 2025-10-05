from .models import Event, User

def admin_context(request):
    """Add admin statistics to context"""
    if request.path.startswith('/admin/'):
        return {
            'events_count': Event.objects.count(),
            'pending_events': Event.objects.filter(status='pending').count(),
            'approved_events': Event.objects.filter(status='approved').count(),
            'users_count': User.objects.count(),
        }
    return {}