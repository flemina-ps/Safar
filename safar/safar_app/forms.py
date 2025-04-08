from django import forms
from .models import Destination, Trip, Itinerary
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'image', 'description', 'category', 'average_cost']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['user', 'destination', 'start_date', 'end_date', 'budget']

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['trip', 'day', 'activities']

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, label='Full Name')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name']
        user.first_name = full_name.split(' ')[0]
        user.last_name = ' '.join(full_name.split(' ')[1:])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }