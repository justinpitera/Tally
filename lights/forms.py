from django import forms
from django.shortcuts import render, redirect

from lights.models import Light


class LightForm(forms.ModelForm):
    class Meta:
        model = Light
        fields = ['bulb_ip', 'name', 'status']
