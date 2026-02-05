"""
Management command to create test users for NAHB.
Usage: python manage.py create_test_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole


class Command(BaseCommand):
    help = 'Creates test users (admin, author, reader) for development'

    def handle(self, *args, **options):
        test_users = [
            {
                'username': 'admin',
                'email': 'admin@nahb.local',
                'password': 'Admin123!',
                'role': UserRole.ADMIN,
                'is_superuser': True,
                'is_staff': True
            },
            {
                'username': 'author1',
                'email': 'author1@nahb.local',
                'password': 'Author123!',
                'role': UserRole.AUTHOR,
                'is_superuser': False,
                'is_staff': False
            },
            {
                'username': 'reader1',
                'email': 'reader1@nahb.local',
                'password': 'Reader123!',
                'role': UserRole.READER,
                'is_superuser': False,
                'is_staff': False
            },
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_superuser': user_data['is_superuser'],
                    'is_staff': user_data['is_staff']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Created user: {user_data['username']} (password: {user_data['password']})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"User already exists: {user_data['username']}"
                ))
            
            # Update profile role
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = user_data['role']
            profile.save()
            self.stdout.write(f"  Role set to: {user_data['role']}")
        
        self.stdout.write(self.style.SUCCESS('\nTest users ready!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:  admin / Admin123!')
        self.stdout.write('  Author: author1 / Author123!')
        self.stdout.write('  Reader: reader1 / Reader123!')
