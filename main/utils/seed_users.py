from django.contrib.auth.models import User, Group
from .permissions import create_limited_users_permission_group

def seed_example_users():
    created = []

    # Ensure the group and its permissions exist
    create_limited_users_permission_group()

    # Create superadmin
    if not User.objects.filter(username='superadmin').exists():
        User.objects.create_superuser('superadmin', 'superadmin@example.com', 'superpass123')
        created.append('superadmin')

    # Create admin user with full permissions
    if not User.objects.filter(username='adminuser').exists():
        admin_user = User.objects.create_user(
            'adminuser', 'admin@example.com', 'adminpass123', is_staff=True
        )
        # Give all permissions to adminuser
        from django.contrib.auth.models import Permission
        admin_user.user_permissions.set(Permission.objects.all())
        created.append('adminuser')

    # Create limited user and assign to LimitedUsers group
    if not User.objects.filter(username='limiteduser').exists():
        limited_user = User.objects.create_user(
            'limiteduser', 'user@example.com', 'userpass123', is_staff=True
        )
        limited_group = Group.objects.get(name='LimitedUsers')  # use existing group
        limited_user.groups.add(limited_group)
        created.append('limiteduser')
        
    # Create no permissions user and assign no permission group
    if not User.objects.filter(username='nopermissionsuser').exists():
        no_permissions_user = User.objects.create_user(
            'nopermissionsuser', 'user@example.com', 'userpass123'
        )
        created.append('nopermissionsuser')

    return created
