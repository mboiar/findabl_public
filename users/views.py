# from re import template
from django.shortcuts import render
#from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from .serializers import UserSerializer
# To make password encryption
# from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from users.models import Preferences
from django.views.generic import View, FormView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from users.forms import RegistrationForm
from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import models
from users.tokens import email_verification_token
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
# from django.db.models import Model
from django.contrib import messages
from django.contrib.auth import views as auth_views
from users.models import Profile

MANUAL_VERIFICATION = False
EMAIL_VERIFICATION = True

# class ProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'users/profile.html'

@method_decorator(ratelimit(key='ip', rate='3/m', method='POST'), name='post')
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    # success_url = '/users/success/'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'users/already_logged_in.html')
        return super().get(self, request)

    def form_valid(self, form):
        self.request.session['activation-required'] = True
        user = form.save(commit=False)
        if EMAIL_VERIFICATION:
            user.is_active = False
            self._send_email_verification(user)
        user.save()
        #handle errors
        return render(self.request, 'registration/registration_done.html')
    
    def _send_email_verification(self, user: User):
        current_site = get_current_site(self.request)
        subject, to = 'Activate Your Account', user.email
        context = {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        html_content = render_to_string(
            'registration/email_verification.html',
            context=context
            )
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, to=[to])
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = "html"
        if not msg.send():
            if not user.is_active: get_user_model().objects.get(pk=user.pk).delete()
            messages.error(self.request, f'Problem sending confirmation email to {to}, check if you typed it correctly.')

class ActivateView(View):
    def get_user_from_email_verification_token(self, uidb64: str, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, OverflowError, get_user_model().DoesNotExist):
            return None
        if user is not None and email_verification_token.check_token(user, token):
            return user
        return None
    
    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        if not user:
            return HttpResponse('The activation was not successful. Get a new activation link or check if your account is already activated.')
        # if MANUAL_VERIFICATION:
        # TODO
        user.is_active = True
        user.save()
        return render(request, "registration_complete.html")

class CustomLoginView(auth_views.LoginView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'users/already_logged_in.html')
        return super().get(self, request)

class CustomLogoutView(auth_views.LogoutView):
    next_page = None
    # template_name = 'users/templates/registration/logged_out.html'

def toggle_mode_preference(request, *args, **kwargs):
    toggle = {"light":"dark", "dark":"light"}
    if request.user.is_authenticated:
        try:
            pref = Preferences.objects.get(user=request.user)
            pref.theme = toggle[(pref.theme)]
            pref.save(update_fields=["theme"])
        except Preferences.DoesNotExist:
            theme = toggle[request.session.get('theme','light')]
            Preferences.objects.create(user=request.user, theme=theme)
    else:
        request.session['theme'] = toggle[request.session.get('theme','light')]
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    # login_url = '/login/'
    """View to delete a ``Profile`` instance."""
    model = Profile
    template_name = 'users/profile_confirm_delete.html'
    success_url = '/users/profile-delete-done/'
    def get_object(self, queryset = ...) -> models.Model:
        return self.request.user

class ProfileDeleteDoneView(TemplateView):
    template_name = 'users/profile_delete_done.html'

class ProfileUpdateView(UpdateView):
    """View to delete a ``Profile`` instance."""
    model = Profile
    template_name = 'users/profile_update.html'
    #success_url = '/'
    # form_class = ProfileUpdateForm
    def form_valid(self, form):
        # update user
        return super().form_valid(form)

class ContributionView(TemplateView):
    template_name = 'users/contribution.html'