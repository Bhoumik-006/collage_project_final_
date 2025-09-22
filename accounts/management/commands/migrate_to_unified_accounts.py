"""
Management command to migrate existing accounts to the unified system.

This command ensures all existing users have both student and organizer profiles,
allowing them to access both functionalities with a single account.

Usage:
    python manage.py migrate_to_unified_accounts
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Migrate existing accounts to unified system with both student and organizer profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating profiles',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get all users
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(
                self.style.SUCCESS('No users found in the database.')
            )
            return

        created_student_profiles = 0
        created_organizer_profiles = 0
        total_users = users.count()

        self.stdout.write(f'Processing {total_users} users...')

        for user in users:
            # Check if user has student profile
            student_profile_exists = UserProfile.objects.filter(
                user=user, user_type='student'
            ).exists()
            
            # Check if user has organizer profile
            organizer_profile_exists = UserProfile.objects.filter(
                user=user, user_type='organizer'
            ).exists()

            # Create missing student profile
            if not student_profile_exists:
                if not dry_run:
                    UserProfile.objects.create(user=user, user_type='student')
                created_student_profiles += 1
                self.stdout.write(f'  Created student profile for: {user.email}')

            # Create missing organizer profile
            if not organizer_profile_exists:
                if not dry_run:
                    UserProfile.objects.create(user=user, user_type='organizer')
                created_organizer_profiles += 1
                self.stdout.write(f'  Created organizer profile for: {user.email}')

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Migration Summary:')
        self.stdout.write(f'  Total users processed: {total_users}')
        self.stdout.write(f'  Student profiles created: {created_student_profiles}')
        self.stdout.write(f'  Organizer profiles created: {created_organizer_profiles}')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nThis was a dry run. Run without --dry-run to apply changes.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\nMigration completed successfully!')
            )
            self.stdout.write(
                'All users now have access to both student and organizer features.'
            )
