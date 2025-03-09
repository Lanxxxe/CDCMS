from django import forms
from landing.models import Announcement, GuardianInfo, StudentEvaluation

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'picture', 'description']
        widgets = {
            # 'posted_by': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class GuardianInfoForm(forms.ModelForm):
     # Define choices for the relationship field
    RELATIONSHIP_CHOICES = [
        ('Parent', 'Parent'),
        ('Guardian', 'Guardian'),
        ('Sibling', 'Sibling'),
        ('Other', 'Other'),
    ]

    # Override the relationship field to use a dropdown
    relationship = forms.ChoiceField(
        choices=RELATIONSHIP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = GuardianInfo
        fields = ['relationship', 'firstName', 'lastName', 'contact_number', 'email']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class StudentEvaluationForm(forms.ModelForm):
    # Override the evaluation_period field to use a dropdown with a class attribute
    evaluation_period = forms.ChoiceField(
        choices=StudentEvaluation.EVALUATION_PERIOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentEvaluation
        fields = [
            'gross_motor_score', 'fine_motor_score', 
            'self_help_score', 'receptive_language_score', 'expressive_language_score', 
            'cognitive_score', 'socio_emotional_score'
        ]
        widgets = {
            'gross_motor_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'fine_motor_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'self_help_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'receptive_language_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'expressive_language_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'cognitive_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
            'socio_emotional_score': forms.NumberInput(attrs={'min': '0', 'max': '20', 'class': 'form-control'}),
        }

        



