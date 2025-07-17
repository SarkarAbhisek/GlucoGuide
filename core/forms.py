from django import forms
from .models import UserProfile, BloodTest, RiskAssessment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'gender', 'height', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BloodTestForm(forms.ModelForm):
    class Meta:
        model = BloodTest
        fields = ['fasting_glucose', 'post_prandial_glucose', 'hba1c', 'random_glucose']
        widgets = {
            'fasting_glucose': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
            'post_prandial_glucose': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
            'hba1c': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
            'random_glucose': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
        }

class RiskAssessmentForm(forms.ModelForm):
    PHYSICAL_ACTIVITY_CHOICES = [
        ('a', 'Exercise (regular) + strenuous work'),
        ('b', 'Exercise (regular) or strenuous work'),
        ('c', 'No Exercise or strenuous work'),
    ]
    
    FAMILY_HISTORY_CHOICES = [
        ('a', 'No family member'),
        ('b', 'Grandparent, aunt, uncle, or first cousin'),
        ('c', 'Brother, sister, or own child'),
        ('d', 'Either parent'),
        ('e', 'Both parents'),
    ]
    
    physical_activity = forms.ChoiceField(choices=PHYSICAL_ACTIVITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    family_history = forms.ChoiceField(choices=FAMILY_HISTORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    waist = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    hypertension = forms.BooleanField(widget=forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}), required=False)
    high_blood_sugar_med = forms.BooleanField(widget=forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}), required=False)
    fruit_intake = forms.BooleanField(widget=forms.Select(choices=[(True, 'Everyday'), (False, 'Not Everyday')], attrs={'class': 'form-control'}), required=False)
    high_blood_glucose = forms.BooleanField(widget=forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}), required=False)
    
    class Meta:
        model = RiskAssessment
        fields = ['physical_activity', 'family_history', 'waist', 'hypertension', 
                 'high_blood_sugar_med', 'fruit_intake', 'high_blood_glucose']