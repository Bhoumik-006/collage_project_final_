# Quick Django template test
# Run this with: python manage.py shell

from django.template.loader import get_template
from django.conf import settings

print("Django Template Settings:")
print(f"Template DIRS: {settings.TEMPLATES[0]['DIRS']}")
print(f"APP_DIRS: {settings.TEMPLATES[0]['APP_DIRS']}")

try:
    template = get_template('organizer-dashboard.html')
    print(f"Template found at: {template.template.name}")
except Exception as e:
    print(f"Template error: {e}")

print("\nTo fix the issue, try:")
print("1. Restart Django server (Ctrl+C then python manage.py runserver)")
print("2. Clear browser cache (Ctrl+F5)")
print("3. Check if you're logged in as the right user type")