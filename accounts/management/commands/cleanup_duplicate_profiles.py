from django.core.management.base import BaseCommand
from django.db.models import Count
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Clean up duplicate UserProfile objects'

    def handle(self, *args, **options):
        # Find users with duplicate profiles
        duplicate_users = UserProfile.objects.values('user').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        deleted_count = 0
        
        for duplicate in duplicate_users:
            user_id = duplicate['user']
            profiles = UserProfile.objects.filter(user_id=user_id).order_by('id')
            
            # Keep the first profile, delete the rest
            profiles_to_delete = profiles[1:]
            for profile in profiles_to_delete:
                self.stdout.write(
                    self.style.WARNING(
                        f'Deleting duplicate profile for user ID {user_id}: {profile.id}'
                    )
                )
                profile.delete()
                deleted_count += 1
        
        if deleted_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} duplicate profiles'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No duplicate profiles found')
            )