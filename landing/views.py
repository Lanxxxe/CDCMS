from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.db import transaction
from .forms import EnrollmentForm
from .models import Student, StudentAddress, FatherInfo, MotherInfo, GuardianInfo, Enrollment
from datetime import datetime
import uuid, re
import sweetify

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'landing/about.html')

def enroll(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            
            try:                
                with transaction.atomic():
                    last_student = Student.objects.filter(student_id__startswith="AY2425").order_by('-student_id').first()

                    if last_student:
                        # Extract the number part from the student_id (e.g., "AY2425-05" -> 5)
                        match = re.search(r"-(\d+)$", last_student.student_id)
                        last_number = int(match.group(1)) if match else 0
                        next_number = last_number + 1  # Increment
                    else:
                        next_number = 1  # Start from 1 if no students exist

                    student_number = f"{next_number:02d}"  # Formats to '01', '02', '03', etc.
                    student_id = f"AY2425-{student_number}"

                    # Create Student
                    student = Student.objects.create(
                        student_id=f"{student_id}",
                        firstName=form.cleaned_data['fName'],
                        middleName=form.cleaned_data['mName'],
                        lastName=form.cleaned_data['lName'],
                        suffix=form.cleaned_data['suffix'],
                        birthdate=form.cleaned_data['bDay'],
                        age=form.cleaned_data['age'],
                        sex=form.cleaned_data['sex'],
                        healthHistory=form.cleaned_data['healthHistory']
                    )

                    # Create StudentAddress
                    StudentAddress.objects.create(
                        student=student,
                        address_no=form.cleaned_data['addressNumber'],
                        baranggay=form.cleaned_data['brgy'],
                        municipality=form.cleaned_data['municipality']
                    )

                    # Create FatherInfo
                    FatherInfo.objects.create(
                        student=student,
                        firstName=form.cleaned_data['fatherFName'],
                        middleName=form.cleaned_data['fatherMName'],
                        lastName=form.cleaned_data['fatherLName'],
                        contact_number=form.cleaned_data['fatherContactNo']
                    )

                    # Create MotherInfo
                    MotherInfo.objects.create(
                        student=student,
                        firstName=form.cleaned_data['motherFName'],
                        middleName=form.cleaned_data['motherMName'],
                        lastName=form.cleaned_data['motherLName'],
                        contact_number=form.cleaned_data['motherContactNo']
                    )

                    # Create GuardianInfo
                    GuardianInfo.objects.create(
                        student=student,
                        firstName=form.cleaned_data['guardianFName'],
                        middleName=form.cleaned_data['guardianMName'],
                        lastName=form.cleaned_data['guardianLName'],
                        contact_number=form.cleaned_data['guardianContactNo'],
                        relationship=form.cleaned_data['guardianRelationship'],
                        email=form.cleaned_data['guardianEmail'],
                        occupation=form.cleaned_data['guardianOccupation']
                    )

                    # Create Enrollment with secure file handling
                    enrollment = Enrollment(
                        student=student,
                        schedule=form.cleaned_data['schedule']
                    )
                    
                    # Securely save each file
                    for field in ['psa', 'immunizationCard', 'recentPhoto', 'guardianQCID']:
                        print(field)
                        if form.cleaned_data[field]:
                            file = form.cleaned_data[field]
                            print(file)
                            field_name = field if field != 'immunizationCard' else 'immunizationCard'
                            file_content = file.read()
                            file_ext = file.name.split('.')[-1]
                            secure_filename = f"{uuid.uuid4().hex}.{file_ext}"
                            # file_path = getattr(enrollment, field_name).field.upload_to(enrollment, secure_filename)
                            getattr(enrollment, field_name).save(secure_filename, file)

                    enrollment.save()
                print('enrollment successful')
                sweetify.success(request, 'Enrollment successful!', persistent="Okay") 
                return redirect('home')  # Redirect to a success page
            except Exception as e:
                # Handle any errors
                print(f"Error: {e}")
                sweetify.error(request, f'An error occurred: {str(e)}', persistent="Okay")
        else:
            # Form is not valid
            print("Form errors:", form.errors)
            sweetify.error(request, 'Please correct the errors in the form.', persistent="Okay")
    else:
        form = EnrollmentForm()
    
    return render(request, 'enrollment.html', {'form': form})

@login_required
def serve_secure_image(request, enrollment_id, image_field):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    # Check if the user has permission to view this enrollment
    if not (request.user.is_staff or request.user == enrollment.student.user):
        raise Http404("Permission denied")
    
    # Get the requested image field
    image = getattr(enrollment, image_field, None)
    if not image:
        raise Http404("Image not found")
    
    # Serve the image
    response = FileResponse(image.open(), content_type='image/jpeg')
    response['Content-Disposition'] = f'inline; filename="{image.name}"'
    return response