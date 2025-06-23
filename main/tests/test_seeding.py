import pytest
from django.contrib.auth.models import User, Group
from main.utils.permissions import create_limited_users_permission_group
from main.utils.seed_users import seed_example_users 

# Seeding is usually considered setup or fixture logic, not core app logic.
# Instead write tests that assume seeded data exists.

@pytest.mark.django_db
def test_seeded_users_exist():
    seed_example_users()
    # List of usernames your seed function creates
    seeded_usernames = ['superadmin', 'adminuser', 'limiteduser', 'nopermissionsuser']
    
    for username in seeded_usernames:
        user = User.objects.filter(username=username).first()
        assert user is not None, f"User {username} should exist"
        
    # Optionally check user properties, e.g. superuser, staff flags
    superadmin = User.objects.get(username='superadmin')
    assert superadmin.is_superuser
    assert superadmin.is_staff
    
    adminuser = User.objects.get(username='adminuser')
    assert adminuser.is_staff and not adminuser.is_superuser

@pytest.mark.django_db
def test_limited_users_group_exists_and_has_permissions():
    create_limited_users_permission_group()
    group_name = 'LimitedUsers'
    group = Group.objects.filter(name=group_name).first()
    assert group is not None, f"Group {group_name} should exist"

    # Check it has some permissions (adjust based on your setup)
    permissions = group.permissions.all()
    assert permissions.exists(), "LimitedUsers group should have permissions assigned"
