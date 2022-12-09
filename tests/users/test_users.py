"""Tests for the `users` app written with pytest"""

import uuid

import pytest
import factory
from pytest_factoryboy import register
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import Preferences
from users.views import toggle_mode_preference

@pytest.fixture
def user_model():
    """Returns current user model defined in settings.py"""
    return get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """Generates instances of the `user` model."""

    class Meta:
        model = get_user_model()
    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")
    password = '11111111'

register(UserFactory)

@pytest.fixture
def test_passwd():
   return 'strong-test-pass'

@pytest.fixture
def auto_login_user(db, client, create_user, test_passwd):
   """Pytest fixture for logging in a user."""

   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_passwd)
       return client, user
   return make_auto_login

@pytest.fixture
def generic_user_data():
    """ A sample place model data for testing purposes"""

    return {
        'username': 'testuser1',
        'email': 'testuser1@gmail.com',
        'password': '1111'
    }

@pytest.fixture
def create_user(db, django_user_model, test_passwd):
    """Pytest fixture for creating an instance of a user."""

    def make_user(**kwargs):
        kwargs['password'] = test_passwd
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_user_create(client, generic_user_data, user_model):
    """Tests user creation."""

    user_model.objects.create_user(**generic_user_data)
    assert user_model.objects.count() == 1

@pytest.mark.django_db
def test_preference_set(client, generic_user_data, user_model):
    """Tests change of user preferences."""

    user = user_model.objects.create_user(**generic_user_data)
    response = client.post(reverse('toggle_mode_preference'))
    assert response.status_code == 301
#   assert
#   toggle_mode_preference()


# TEST AUTHENITCATION
@pytest.mark.django_db
def test_auth_view(auto_login_user):
    """Tests user login."""

    client, user = auto_login_user()
    url = reverse('reg:login')
    response = client.get(url)
    assert response.status_code == 301

# @pytest.mark.django_db
# def test_send_verification_link(auto_login_user, mailoutbox):
#     pass
#    client, user = auto_login_user()
#    url = reverse('send-')
#    response = client.post(url)
#    assert response.status_code == 201
#    assert len(mailoutbox) == 1
#    mail = mailoutbox[0]
#    assert mail.subject == f'Report to {user.email}'
#    assert list(mail.to) == [user.email]