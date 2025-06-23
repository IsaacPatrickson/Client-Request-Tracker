import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from main.models import Client
from main.utils.permissions import create_limited_users_permission_group

@pytest.mark.django_db
def test_limited_user_permissions(client, django_user_model):
    # Set up permissions and user
    group = create_limited_users_permission_group()
    user = django_user_model.objects.create_user(username='limited', password='secure123', is_staff=True)
    user.groups.add(group)
    client.login(username='limited', password='secure123')

    # View Client list (changelist)
    changelist_url = reverse('admin:main_client_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200

    # Add a new client
    add_url = reverse('admin:main_client_add')
    response = client.post(add_url, {
        'name': 'Test Client',
        'email': 'test@example.com',
        'contact_number': '0123456789',
        'company_url': 'https://example.com',
        'is_active': True
    })
    assert response.status_code == 302  # Redirect on success
    assert Client.objects.filter(name='Test Client').exists()

    # Get the created client
    client_obj = Client.objects.get(name='Test Client')

    # Change/edit the client
    change_url = reverse('admin:main_client_change', args=[client_obj.pk])
    response = client.post(change_url, {
        'name': 'Updated Client',
        'email': 'test@example.com',
        'contact_number': '0123456789',
        'company_url': 'https://example.com',
        'is_active': True
    })
    assert response.status_code == 302
    assert Client.objects.filter(name='Updated Client').exists()

    # Attempt to delete (should be forbidden)
    delete_url = reverse('admin:main_client_delete', args=[client_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_limited_user_permissions():
    # Assuming your create_limited_users_permission_group function is imported and available
    group = create_limited_users_permission_group()

    # Check group has the correct permissions for models
    expected_models = ['client', 'requesttype', 'clientrequest']
    expected_actions = ['view', 'add', 'change']

    for model in expected_models:
        content_type = ContentType.objects.get(app_label='main', model=model)
        
        # Check for view/add/change permissions
        for action in expected_actions:
            codename = f"{action}_{model}"
            perm = group.permissions.filter(content_type=content_type, codename=codename)
            assert perm.exists(), f"Group missing permission: {codename}"

        # Check that delete permission is NOT present
        delete_codename = f"delete_{model}"
        delete_perm = group.permissions.filter(content_type=content_type, codename=delete_codename)
        assert not delete_perm.exists(), f"Group should NOT have permission: {delete_codename}"

@pytest.mark.django_db
def test_limited_user_cannot_delete(client):
    # Setup user and assign to LimitedUsers group
    group = create_limited_users_permission_group()
    user = User.objects.create_user(username='limitedadmin', password='testpass')
    user.groups.add(group)
    user.save()

    # Log in as limited admin user
    client.login(username='limitedadmin', password='testpass')

    # Pick a model and try to delete an object through admin or API
    # For example, try deleting a Client object via admin panel
    # Create an instance to attempt deletion
    from main.models import Client
    client_instance = Client.objects.create(name='Test Client', email='test@example.com')

    # Attempt to delete client via Django admin URL
    # The admin delete URL for Client typically looks like:
    # /admin/main/client/<id>/delete/
    delete_url = reverse('admin:main_client_delete', args=[client_instance.pk])
    response = client.get(delete_url)

    # The user should get forbidden or redirect to login (usually 403 or 302)
    assert response.status_code in (302, 403), "Limited admin should not access delete page"