from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, UserProfile, Event
from .forms import DenyEventForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms

# Custom Event Admin Form
class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control status-dropdown',
                'style': 'min-width: 200px; padding: 8px 12px; font-size: 14px; border-radius: 6px;'
            }),
            'denial_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'min-width: 400px; min-height: 100px; padding: 10px; font-size: 14px; border-radius: 6px;',
                'rows': 4,
                'placeholder': 'Enter reason for denial (if applicable)...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'style': 'width: 100%; padding: 10px;'
            }),
            'additional_details': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 10px;'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 10px;'
            }),
            'prizes': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 10px;'
            }),
        }

# Unregister the Group model since we don't need it for this project
admin.site.unregister(Group)

class CustomAdminSite(AdminSite):
    """Custom admin site with enhanced dashboard"""
    
    def index(self, request, extra_context=None):
        """Custom admin index with statistics"""
        extra_context = extra_context or {}
        
        # Add statistics to the context
        extra_context.update({
            'events_count': Event.objects.count(),
            'pending_events': Event.objects.filter(status='pending').count(),
            'approved_events': Event.objects.filter(status='approved').count(),
            'users_count': User.objects.count(),
        })
        
        return super().index(request, extra_context)

# Use custom admin site
admin_site = CustomAdminSite(name='custom_admin')

class UserProfileInline(admin.StackedInline):
    """
    Allows editing UserProfile directly within the User admin page.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    extra = 0  # Don't show extra empty forms


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin to display the UserProfile inline.
    """
    inlines = (UserProfileInline, )
    
    # Customize the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def get_user_type(self, obj):
        """Get user type from related UserProfile"""
        try:
            # Get all profiles for this user using the correct related_name
            profiles = obj.profiles.all()
            if profiles.exists():
                # If multiple profiles, show all types
                user_types = [profile.user_type for profile in profiles]
                return ', '.join(user_types)
            else:
                return 'No Profile'
        except Exception as e:
            return 'Error'
    get_user_type.short_description = 'User Type'


class UserProfileAdmin(admin.ModelAdmin):
    """
    Custom admin for UserProfile with better organization
    """
    list_display = ('user', 'user_type', 'contact_number', 'get_email')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email', 'contact_number')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

# Customize admin site headers and titles
admin.site.site_header = "StudentConnect Admin"
admin.site.site_title = "StudentConnect"
admin.site.index_title = "Event Management Dashboard"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm  # Use custom form
    list_display = ('title', 'category', 'organizer', 'date', 'status_display', 'image_preview', 'get_deletion_status', 'get_denial_reason', 'styling_applied', 'days_since_submission')
    list_filter = ('status', 'category', 'date', 'styling_applied', 'deleted_at', 'is_featured')
    search_fields = ('title', 'description', 'organizer__user__username', 'organizer__user__email')
    actions = ['approve_events', 'deny_events', 'delete_events', 'feature_events', 'bulk_approve_pending']
    ordering = ('-date', 'status')
    readonly_fields = ('image_preview_large', 'featured_image_preview', 'submission_info')
    list_per_page = 25
    
    # Remove custom CSS to use default Django admin styling
    # class Media:
    #     css = {
    #         'all': ('admin/css/custom_admin.css?v=2.0',)
    #     }
    #     js = ('admin/js/custom_admin.js',)

    fieldsets = (
        ('📝 Event Information', {
            'fields': ('title', 'description', 'category', 'date', 'time', 'location', 'organizer')
        }),
        ('🖼️ Event Media', {
            'fields': ('event_flyer', 'image_preview_large', 'event_link'),
            'classes': ('wide',),
            'description': 'Event flyer uploaded by organizer and registration link.'
        }),
        ('🔗 Additional Details', {
            'fields': ('contact_email', 'additional_details', 'requirements', 'prizes'),
            'classes': ('wide',),
            'description': 'Optional additional information to help students understand the event better.'
        }),
        ('✅ Approval Status', {
            'fields': ('status', 'denial_reason', 'submission_info'),
            'classes': ('wide',),
        }),
        ('🗑️ Deletion Tracking', {
            'fields': ('deleted_at', 'deleted_by'),
            'classes': ('collapse',),
            'description': 'Tracks when and by whom the event was deleted.'
        }),
        ('🎨 Auto-Styling (Applied on Approval)', {
            'fields': ('featured_image', 'featured_image_preview', 'color_theme', 'styling_applied', 'is_featured'),
            'classes': ('collapse',),
            'description': 'These fields are automatically filled when an event is approved.'
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('deny/<int:event_id>/', self.admin_site.admin_view(self.deny_event_view), name='deny-event'),
        ]
        return custom_urls + urls

    def get_denial_reason(self, obj):
        if obj.status == 'denied' and obj.denial_reason:
            return obj.denial_reason[:50] + '...' if len(obj.denial_reason) > 50 else obj.denial_reason
        return '-'
    get_denial_reason.short_description = 'Denial Reason'
    
    def get_deletion_status(self, obj):
        if obj.is_deleted:
            return f"🗑️ Deleted on {obj.deleted_at.strftime('%Y-%m-%d %H:%M')} by {obj.deleted_by.username if obj.deleted_by else 'Unknown'}"
        return "✅ Active"
    get_deletion_status.short_description = 'Status'

    def approve_events(self, request, queryset):
        approved_count = 0
        for event in queryset:
            event.status = 'approved'
            event.denial_reason = ''
            event.save()  # Save first to update status
            event.apply_auto_styling()  # Then apply auto-styling
            approved_count += 1
        
        self.message_user(request, f"{approved_count} events have been approved and auto-styled.")
    approve_events.short_description = "Approve and auto-style selected events"

    def deny_events(self, request, queryset):
        if queryset.count() == 1:
            event = queryset.first()
            return HttpResponseRedirect(f"deny/{event.id}/")
        self.message_user(request, "Please select only one event to deny at a time.", level='ERROR')
    deny_events.short_description = "Deny selected event"

    def delete_events(self, request, queryset):
        deleted_count = 0
        event_titles = []
        
        for event in queryset:
            event_titles.append(event.title)
            # Soft delete the event instead of hard delete
            event.soft_delete(deleted_by_user=request.user)
            deleted_count += 1
        
        if deleted_count == 1:
            self.message_user(request, f"Event '{event_titles[0]}' has been marked as deleted.")
        else:
            self.message_user(request, f"{deleted_count} events have been marked as deleted: {', '.join(event_titles)}")
    delete_events.short_description = "🗑️ Mark selected events as deleted"

    def feature_events(self, request, queryset):
        """Mark selected approved events as featured"""
        featured_count = 0
        for event in queryset.filter(status='approved'):
            event.is_featured = True
            event.save()
            featured_count += 1
        
        self.message_user(request, f"{featured_count} events have been marked as featured.")
    feature_events.short_description = "⭐ Mark as featured events"

    def bulk_approve_pending(self, request, queryset):
        """Bulk approve all pending events with auto-styling"""
        pending_events = queryset.filter(status='pending')
        approved_count = 0
        
        for event in pending_events:
            event.status = 'approved'
            event.denial_reason = ''
            event.save()
            event.apply_auto_styling()
            approved_count += 1
        
        self.message_user(request, f"{approved_count} pending events have been approved and auto-styled.")
    bulk_approve_pending.short_description = "🚀 Bulk approve pending events"

    def days_since_submission(self, obj):
        """Show how many days since event was submitted"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Use creation timestamp from the model (you might need to add this field)
        # For now, we'll estimate based on the event date
        today = timezone.now().date()
        days_diff = (today - obj.date).days
        
        if days_diff < 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">📅 Future event</span>')
        elif days_diff == 0:
            return format_html('<span style="color: #ffc107; font-weight: bold;">📅 Today</span>')
        elif days_diff <= 7:
            return format_html('<span style="color: #17a2b8;">📅 {} days ago</span>', days_diff)
        else:
            return format_html('<span style="color: #6c757d;">📅 {} days ago</span>', days_diff)
    days_since_submission.short_description = 'Submitted'

    def submission_info(self, obj):
        """Display submission and approval information"""
        info_lines = []
        
        # Organizer info
        info_lines.append(f"👤 Submitted by: <strong>{obj.organizer.user.get_full_name() or obj.organizer.user.username}</strong>")
        info_lines.append(f"📧 Contact: {obj.organizer.user.email}")
        
        # Status info
        if obj.status == 'pending':
            info_lines.append('<span style="color: #ffc107;">⏳ Awaiting approval</span>')
        elif obj.status == 'approved':
            info_lines.append('<span style="color: #28a745;">✅ Approved and published</span>')
        elif obj.status == 'denied':
            info_lines.append('<span style="color: #dc3545;">❌ Denied - requires revision</span>')
        
        # Event timing
        from django.utils import timezone
        today = timezone.now().date()
        if obj.date >= today:
            days_until = (obj.date - today).days
            if days_until == 0:
                info_lines.append('<span style="color: #ffc107; font-weight: bold;">📅 Event is today!</span>')
            elif days_until <= 7:
                info_lines.append(f'<span style="color: #17a2b8;">📅 Event in {days_until} days</span>')
            else:
                info_lines.append(f'📅 Event in {days_until} days')
        else:
            info_lines.append('<span style="color: #6c757d;">📅 Past event</span>')
        
        return format_html('<br>'.join(info_lines))
    submission_info.short_description = 'Submission Details'

    def deny_event_view(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if request.method == 'POST':
            form = DenyEventForm(request.POST)
            if form.is_valid():
                event.status = 'denied'
                event.denial_reason = form.cleaned_data['denial_reason']
                event.save()
                self.message_user(request, "Event has been denied.")
                return HttpResponseRedirect("../../")
        else:
            form = DenyEventForm()

        context = {
            'event': event,
            'form': form,
            'opts': self.model._meta,
            'title': f"Deny Event: {event.title}",
        }
        return render(request, 'admin/deny_event.html', context)
    
    def status_display(self, obj):
        """Display status with colored indicators"""
        if obj.status == 'pending':
            return format_html(
                '<span style="background-color: #ffc107; color: #212529; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">⏳ PENDING</span>'
            )
        elif obj.status == 'approved':
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">✅ APPROVED</span>'
            )
        elif obj.status == 'denied':
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">❌ DENIED</span>'
            )
        return obj.status.upper()
    status_display.short_description = 'Status'
    
    def image_preview(self, obj):
        """Small image preview for list display"""
        if obj.event_flyer:
            return format_html(
                '<a href="{}" target="_blank" title="Click to view full size">'
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd; cursor: pointer;" title="{}"/>'
                '</a>',
                obj.event_flyer.url,
                obj.event_flyer.url,
                obj.title
            )
        return "No Image"
    image_preview.short_description = '🖼️ Image'
    
    def image_preview_large(self, obj):
        """Large image preview for detail view"""
        if obj.event_flyer:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" title="Click to view full size">'
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain; border: 2px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); cursor: pointer;" />'
                '</a>'
                '<br><small style="color: #666; margin-top: 5px; display: block;">👤 Uploaded by: <strong>{}</strong></small>'
                '<br><small style="color: #666;">📁 File: {}</small>'
                '<br><small style="color: #666;">💾 Size: {} bytes</small>'
                '</div>',
                obj.event_flyer.url,
                obj.event_flyer.url,
                obj.organizer.user.username if obj.organizer else 'Unknown',
                obj.event_flyer.name.split('/')[-1] if obj.event_flyer.name else 'N/A',
                obj.event_flyer.size if hasattr(obj.event_flyer, 'size') else 'Unknown'
            )
        return format_html('<div style="padding: 20px; text-align: center; color: #999; border: 2px dashed #ddd; border-radius: 8px;">📷 No image uploaded by organizer</div>')
    image_preview_large.short_description = '🖼️ Uploaded Event Flyer'
    
    def featured_image_preview(self, obj):
        """Preview of the auto-generated featured image"""
        if obj.featured_image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" title="Click to view full size">'
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border: 2px solid #28a745; border-radius: 8px; cursor: pointer;" />'
                '</a>'
                '<br><small style="color: #28a745; margin-top: 5px; display: block;">✅ Auto-generated featured image</small>'
                '<br><small style="color: #666;">🔗 Source: {}</small>'
                '</div>',
                obj.featured_image,
                obj.featured_image,
                'Organizer Upload' if obj.event_flyer else 'Stock Image'
            )
        return format_html('<div style="padding: 15px; text-align: center; color: #999; border: 2px dashed #ddd; border-radius: 8px;">⏳ Generated after approval</div>')
    featured_image_preview.short_description = '🌟 Featured Image (Auto-Generated)'