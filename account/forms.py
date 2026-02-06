from django import forms
from django.contrib.auth.forms import UserCreationForm

# We can extend this later if we need custom fields like 'phone number'
class UserRegistrationForm(UserCreationForm):
    pass
