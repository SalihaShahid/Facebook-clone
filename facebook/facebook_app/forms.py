from django import forms
from .models import *
from django.contrib.auth.password_validation import validate_password


class SignUpForm(forms.Form):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    email = forms.EmailField(label="Email")
    name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=gender_choices)
    profile_picture=forms.ImageField()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

	


class AuthenticationForm(forms.Form):
	email=forms.EmailField(label="Email")
	verification_code=forms.CharField(max_length=6)

class LoginForm(forms.Form):
	email=forms.EmailField(label="Email")
	password=forms.CharField(widget=forms.PasswordInput())


class SearchForm(forms.Form):
	search=forms.CharField(label="")


class ChatForm(forms.Form):
    message=forms.CharField(label="")

class TextPostForm(forms.Form):
    content=forms.CharField(label="")

class MediaPostForm(forms.Form):
    content=forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','gif','mp4'])])
    caption=forms.CharField(required=False)

class CommentForm(forms.Form):
    comment=forms.CharField()

class TextStoryForm(forms.Form):
    content=forms.CharField(label="")

class MediaStoryForm(forms.Form):
    content=forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','gif','mp4'])])
    caption=forms.CharField(required=False)