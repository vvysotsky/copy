from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('external_id','name', 'coach_information',)
        widgets = { 'name': forms.TextInput, 'coach_information': forms.TextInput,}
