from django.core.validators import RegexValidator
from django import forms


class EnrollmentForm(forms.Form):
    lName = forms.CharField(
        label="Last Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    fName = forms.CharField(
        label="First Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    mName = forms.CharField(
        label="Middle Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    suffix = forms.CharField(
        label="Suffix (if applicable)",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    bDay = forms.DateField(
        label="Birthdate",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )
    sex = forms.ChoiceField(
        label="Sex",
        choices=[("", "Select Sex"), ("Male", "Male"), ("Female", "Female")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    healthHistory = forms.CharField(
        label="Health History (if applicable)",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )

    # Address
    addressNumber = forms.CharField(
        label="Address Number",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    brgy = forms.CharField(
        label="Barangay",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    municipality = forms.CharField(
        label="Municipality",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )

    # Parent/Guardian Information
    fatherLName = forms.CharField(
        label="Father's Last Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    fatherFName = forms.CharField(
        label="Father's First Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    fatherMName = forms.CharField(
        label="Father's Middle Name",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    fatherContactNo = forms.CharField(
        label="Father's Contact Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )

    motherLName = forms.CharField(
        label="Mother's Last Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    motherFName = forms.CharField(
        label="Mother's First Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    motherMName = forms.CharField(
        label="Mother's Middle Name",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    motherContactNo = forms.CharField(
        label="Mother's Contact Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )

    guardian_type = forms.ChoiceField(
        label="Guardian Type",
        choices=[("father", "Father"), ("mother", "Mother"), ("other", "Other")],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial="other"
    )

    guardianLName = forms.CharField(
        label="Guardian's Last Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianFName = forms.CharField(
        label="Guardian's First Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianMName = forms.CharField(
        label="Guardian's Middle Name",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianContactNo = forms.CharField(
        label="Guardian's Contact Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianRelationship = forms.ChoiceField(
        label="Relationship",
        choices=[("", "Select Relationship"), ("Parent", "Parent"), ("Sibling", "Sibling"), ("Grandparent", "Grandparent"), ("Relatives", "Relatives")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    guardianEmail = forms.EmailField(
        label="Guardian's Email",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianOccupation = forms.CharField(
        label="Guardian's Occupation",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )

    # Enrollment Information
    schedule = forms.ChoiceField(
        label="Preferred Schedule",
        choices=[("", "Select Schedule"), ("K1 (3y/o)- 8:00am- 10:00am", "K1 (3y/o)- 8:00am- 10:00am"), ("K2 (4y/o)- 10:15am-12:15nn", "K2 (4y/o)- 10:15am-12:15nn"), ("K3 (4y/o)- 1:30pm-3:30pm", "K3 (4y/o)- 1:30pm-3:30pm")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # File Upload Fields
    psa = forms.ImageField(
        label="PSA Birth Certificate",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'})
    )
    immunizationCard = forms.ImageField(
        label="Immunization Card",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'})
    )
    recentPhoto = forms.ImageField(
        label="Recent Photo",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'})
    )
    guardianQCID = forms.ImageField(
        label="Guardian QC ID",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'})
    )