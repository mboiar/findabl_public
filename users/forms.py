from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms

class RegistrationForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].required = True
#         self.fields['username'].error_messages = {'invalid': 'foobar'}
    email = forms.EmailField(required=True)
    # first_name = forms.CharField(label="")
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("User with provided email already exists. To register a new account, use a unique email address.")
       return self.cleaned_data
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2', )