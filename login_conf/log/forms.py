from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ['username', 'email', 'password1', 'password2']

    # Check unique email
    # Email exists && account active -> email_already_registered
    # Email exists && account not active -> delete previous account and register new one
    def clean_email(self):
        email_passed = self.cleaned_data.get("email")
        email_already_registered = User.objects.filter(email = email_passed).exists()
        user_is_active = User.objects.filter(email = email_passed, is_active = 1)
        if email_already_registered and user_is_active:
            #print('email_already_registered and user_is_active')
            raise forms.ValidationError("Email already registered.")
        elif email_already_registered:
            #print('email_already_registered')
            User.objects.filter(email = email_passed).delete()

        return email_passed
