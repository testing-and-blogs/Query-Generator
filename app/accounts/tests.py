import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User

# Mark all tests in this module as Django DB tests
pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    """A client for making API requests."""
    return APIClient()

def test_user_registration(api_client):
    """
    Ensure a new user can be registered via the API.
    """
    url = reverse('user-register')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'strongpassword123'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == 'newuser'

def test_user_login(api_client):
    """
    Ensure a registered user can log in and receive an auth token.
    """
    # First, create a user to log in with
    user = User.objects.create_user(username='testuser', password='password123')

    # Now, attempt to log in
    url = reverse('user-login')
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert response.data['token'] is not None

def test_user_login_invalid_credentials(api_client):
    """
    Ensure login fails with incorrect credentials.
    """
    User.objects.create_user(username='testuser', password='password123')

    url = reverse('user-login')
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in response.data
