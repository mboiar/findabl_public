from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as user_views

user_patterns = ([
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', user_views.ActivateView.as_view(), name='activate'),
    path('contribution/', user_views.ContributionView.as_view(), name='contribution'),
    path('profile-delete/', user_views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('profile-delete-done/', user_views.ProfileDeleteDoneView.as_view(), name='profile_delete_done'),
], 'users')


registration_patterns = ([
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html', success_url='/password-change-done/'), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html', success_url='/password-reset-done/', email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/password-reset-complete/'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

], 'registration')
