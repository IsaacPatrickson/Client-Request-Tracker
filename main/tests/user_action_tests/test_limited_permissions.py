import pytest
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from main.models import Client, RequestType
from main.utils.permissions import create_limited_users_permission_group

@pytest.mark.django_db
def test_limited_user_client_CRUD_permissions(client, django_user_model):
    from bs4 import BeautifulSoup
    
    # Set up permissions and user
    group = create_limited_users_permission_group()
    user = django_user_model.objects.create_user(username='limited', password='secure123', is_staff=True)
    user.groups.add(group)
    client.login(username='limited', password='secure123')

    # View Client list (changelist)
    changelist_url = reverse('admin:main_client_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200

    # Get form first
    add_url = reverse('admin:main_client_add')
    response = client.get(add_url)
    assert response.status_code == 200
    
    # Parse hidden inputs
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Add a new client
    response = client.post(add_url, {
        'csrfmiddlewaretoken': csrf_token,
        'name': 'Test Client',
        'email': 'test@example.com',
        'contact_number': '0123456789',
        'company_url': 'https://example.com',
        'is_active': 'on',
        '_save': 'Save',
        # Required for inlines
        'clientrequest_set-TOTAL_FORMS': 0,
        'clientrequest_set-INITIAL_FORMS': 0,
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
        'is_active': False,
        # Required again for inlines
        'clientrequest_set-TOTAL_FORMS': 0,
        'clientrequest_set-INITIAL_FORMS': 0,
        '_save': 'Save'
    })
    assert response.status_code == 302
    assert Client.objects.filter(name='Updated Client').exists()

    # Attempt to delete (should be forbidden)
    delete_url = reverse('admin:main_client_delete', args=[client_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403
    
@pytest.mark.django_db
def test_limited_user_request_type_CRUD_permissions(client, django_user_model):
    # Set up permissions and user
    group = create_limited_users_permission_group()
    user = django_user_model.objects.create_user(username='limited', password='secure123', is_staff=True)
    user.groups.add(group)
    client.login(username='limited', password='secure123')

    # View Client list (changelist)
    changelist_url = reverse('admin:main_requesttype_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200

    # Add a new client
    add_url = reverse('admin:main_requesttype_add')
    response = client.post(add_url, {
        'name': 'Test Request Type',
        'description': 'Test Description'
    })
    assert response.status_code == 302  # Redirect on success
    assert RequestType.objects.filter(name='Test Request Type').exists()

    # Get the created client
    request_type_obj = RequestType.objects.get(name='Test Request Type')

    # Change/edit the client
    change_url = reverse('admin:main_requesttype_change', args=[request_type_obj.pk])
    response = client.post(change_url, {
        'name': 'Updated Test Request Type',
        'description': 'Updated Test Description'
    })
    assert response.status_code == 302
    assert RequestType.objects.filter(name='Updated Test Request Type').exists()

    # Attempt to delete (should be forbidden)
    delete_url = reverse('admin:main_requesttype_delete', args=[request_type_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403
    
models = ['client', 'requesttype', 'clientrequest']
actions = ['view', 'add', 'change']

@pytest.mark.django_db
def test_limited_user_permissions_check():
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