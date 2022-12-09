from django.urls import re_path, include, path

from places import views as place_views

place_patterns = ([
    path('', place_views.HomeView.as_view(), name='home'),
    path('<int:pk>/', place_views.PlaceDetailView.as_view(), name='place'),
    path('<int:pk>/rate/', place_views.ReviewCreateView.as_view(), name='rate'),
    path('<int:pk>/update/', place_views.ReviewUpdateView.as_view(), name='edit_review'),
    path('<int:pk>/delete/', place_views.ReviewDeleteView.as_view(), name='delete_review'),
    path('filter/', place_views.filter_search, name='filter_search'),
    path('about/', place_views.AboutView.as_view(), name='about'),
    path('search/', place_views.SearchResultsView.as_view(), name='search_results'),
], 'places')
