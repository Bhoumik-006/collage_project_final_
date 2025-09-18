from django.core.management.base import BaseCommand
from accounts.models import Event

class Command(BaseCommand):
    help = 'Debug event images'

    def handle(self, *args, **options):
        events = Event.objects.all()
        print(f"Total events: {events.count()}")
        
        for event in events:
            print(f"\nEvent: {event.title}")
            print(f"  Status: {event.status}")
            print(f"  Event flyer: {event.event_flyer}")
            print(f"  Event flyer exists: {bool(event.event_flyer)}")
            if event.event_flyer:
                print(f"  Event flyer URL: {event.event_flyer.url}")
                print(f"  Event flyer path: {event.event_flyer.path}")
            print(f"  Featured image: {event.featured_image}")
            print(f"  Styling applied: {event.styling_applied}")