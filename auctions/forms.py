from django import forms
from .models import User, auctionListing, Bid, Comment
from django.contrib.auth.forms import UserCreationForm

class createForm(forms.ModelForm):
    class Meta:
        model = auctionListing
        fields = ['name', 'category', 'details', 'price', 'ending_date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter details'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'ending_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter date format YYYY-MM-DD'}),
            'image': forms.FileInput(attrs={'class': 'form-control','id': 'images', 'placeholder': 'Enter image'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        widgets = {
            'bid_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter bid amount'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter comment'}),
        }
