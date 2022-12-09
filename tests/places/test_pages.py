"""
Tests for the `places` app written with pytest
"""

import pytest
import factory
import factory.random
from pytest_factoryboy import register
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import get_user_model

from tests.users.test_users import UserFactory
from places.models import Review, Place

@pytest.fixture
def generic_place_data():
   """ A sample place model data for testing purposes"""

   return {
      'name': 'AnyPlace',
      'location': 'WAW',
      'url': 'https://www.maps.google.com/123232',
      'address': 'Unnamed Road',
      'type': 'BAR',
}

@pytest.fixture
def generic_review_data():
   """ A sample review model data for testing purposes"""

   return {
      'sin': 1,
      'wac': 2,
      'noi': 3,
      'lsi': 4
}
  
User = get_user_model()

class PlaceFactory(factory.django.DjangoModelFactory):
   """Generates dummy instances of `place` model"""

   class Meta:
      model = Place
   name = 'testplace'
   address = factory.LazyAttribute(lambda obj: f"{obj.name}_address")
   url = factory.LazyAttribute(lambda obj: f"http://maps.google.com/{obj.name}")
   location = factory.fuzzy.FuzzyChoice(Place.LOCATION_CHOICES, getter=lambda c: c)
   type = factory.fuzzy.FuzzyChoice(Place.TYPE_CHOICES, getter=lambda c: c)
   
register(PlaceFactory)

class ReviewFactory(factory.django.DjangoModelFactory):
   """Generates dummy instances of `review` model"""

   class Meta:
      model = Review
   sin, wac, noi, lsi = 1, 2, 3, 4
   user = factory.SubFactory(UserFactory)
   place = factory.SubFactory(PlaceFactory)

register(ReviewFactory)

@pytest.mark.django_db
def test_review_factory(review_factory):
   review = review_factory()
   # assert review

@pytest.mark.django_db
def test_home(client):
   """Tests home page"""

   url = reverse('places:home')
   response = client.get(url)
   assert response.status_code == 301

def test_invalid_url_name(client):
   with pytest.raises(NoReverseMatch):
      url = reverse('invalid_url_name')

#TEST REVIEW
@pytest.mark.django_db
def test_review_create(generic_user_data, generic_place_data, generic_review_data):
  """Tests the creation of reviews"""

  user = User.objects.create_user(**generic_user_data)
  place = Place.objects.create(**generic_place_data)
  Review.objects.create(user=user, place=place, **generic_review_data)
  assert Review.objects.count() == 1

# TEST PAGES
@pytest.mark.django_db
def test_place_detail(client, generic_place_data):
   """Tests place detail page"""

   place = Place.objects.create(**generic_place_data)
   url = reverse(
       'places:place', kwargs={'pk': place.pk}
   )
   response = client.get(url)
   assert response.status_code == 301
   print(response.content)
   assert place.name in str(response.content)

@pytest.mark.django_db
def test_search_results(client, generic_place_data):
   """Tests search results page."""
   place = Place.objects.create(**generic_place_data)
   url = reverse(
       'places:place', kwargs={'pk': place.pk}
   )
   response = client.get(url)
   assert response.status_code == 301
   print(response.content)
   assert place.name in str(response.content)

# TEST LANGUAGES
@pytest.mark.django_db
@pytest.mark.parametrize("language_code, text", [
   ('en', 'Hello'),
   ('pl', 'Cześć'),
])
def test_languages(language_code, text, client):
   """Tests internationalization"""
   url = reverse('users:contribution')
   client.cookies["django_language"] = language_code
   response = client.get(url)
   assert response.status_code == 301
   #TODO: test response text with language cookie set
   # assert text in str(response.content)
   # print(response.headers)

# TEST FILTER SEARCH
