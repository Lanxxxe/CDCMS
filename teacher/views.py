from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, CharField, F, Q
from django.db.models.functions import Concat
from landing.models import Student, GuardianInfo, Enrollment, Announcement
from .forms import AnnouncementForm, GuardianInfoForm
import sweetify

def dashboard(request):
    student_count = Student.objects.count()
    print(student_count)
    data = {
        'student_count' : student_count
    }
    return render(request, 'teacher_dashboard.html', data)

def profile(request):
    return render(request, "teacher/profile.html")

def student_management(request):
    # Query to fetch the required data (without images)
    students_data = Student.objects.annotate(
        guardian_name=Case(
            When(guardianinfo__isnull=False, then=Concat(
                F('guardianinfo__lastName'), Value(', '),
                F('guardianinfo__firstName'),
                output_field=CharField()
            )),
            default=Value('No Guardian'),
            output_field=CharField()
        )
    ).values(
        'id',
        'student_id',
        'firstName',
        'middleName',
        'lastName',
        'guardian_name',
        'healthHistory',
        'enrollment__schedule'
    )

    # Step 2: Query the Enrollment Data (Images) Separately
    for student in list(students_data):
        enrollment_data = Enrollment.objects.filter(student_id=student['id']).values(
            'psa', 'immunizationCard', 'recentPhoto', 'guardianQCID'
        ).first()

        # Step 3: Determine Requirements Status
        if enrollment_data:
            # print(enrollment_data['psa'], enrollment_data['guardianQCID'],
            #     enrollment_data['immunizationCard'], enrollment_data['recentPhoto'])
            # Check if all required files are present
            if (enrollment_data['psa'] and enrollment_data['guardianQCID'] and
                enrollment_data['immunizationCard'] and enrollment_data['recentPhoto']):
                student['requirements_status'] = 'Complete'
            else:
                student['requirements_status'] = 'Incomplete'
        else:
            student['requirements_status'] = 'Incomplete'

    # Pass the data to the template
    context = {
        'students': students_data
    }
    print(students_data)
    return render(request, 'teacher/student_management.html', context)

def guardian_management(request):
    guardians = GuardianInfo.objects.select_related('student').all()

    data = {
        'guardians' : guardians,
    }

    return render(request, 'teacher/guardian_management.html', data)

def update_guardian(request, id):
    # Fetch the guardian record to update
    guardian = get_object_or_404(GuardianInfo, id=id)

    if request.method == 'POST':
        # Populate the form with the submitted data and the existing guardian instance
        form = GuardianInfoForm(request.POST, instance=guardian)
        if form.is_valid():
            try:
                # Save the updated guardian information
                form.save()
                
                # Show a success message
                sweetify.success(request, 'Guardian information updated successfully!', persistent="Okay")
                return redirect('guardian_management')  # Redirect to the guardian management page
            
            except Exception as e:
                # Log the error (optional)
                print(f"Error updating guardian: {e}")
                
                # Show an error message to the user
                sweetify.error(request, 'An error occurred while updating the guardian information. Please try again.', persistent="Okay")
        else:
            # If the form is not valid, show an error message
            sweetify.error(request, 'Invalid form data. Please check the fields and try again.', persistent="Okay")
    else:
        # Populate the form with the existing guardian data
        form = GuardianInfoForm(instance=guardian)
    
    return render(request, 'teacher_guardian/update_guardian.html', {'form': form, 'guardian': guardian})


def teacher_management(request):
    return render(request, 'teacher/teacher_management.html')

def announcement(request):
    announcements = Announcement.objects.all().values(
        'id', 'posted_by', 'title', 'picture', 'upload_date', 'description', 'date_posted'
    )
    context = {
        'announcements' : announcements
    }
    return render(request, 'teacher/announcement.html', context)


def add_announcement(request):
    if request.method == 'POST':
        user = "Teacher Theresa"
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the announcement but don't commit to the database yet
                announcement = form.save(commit=False)
                announcement.posted_by = user  # Set the posted_by field
                announcement.save()  # Save to the database
                
                # Show a success message
                sweetify.success(request, 'New Announcement has been added!', persistent="Okay")
                return redirect('announcement')  # Redirect to the announcements list page
            
            except Exception as e:
                # Log the error (optional)
                print(f"Error saving announcement: {e}")
                
                # Show an error message to the user
                sweetify.error(request, 'An error occurred while saving the announcement. Please try again.', persistent="Okay")
        else:
            # If the form is not valid, show an error message
            sweetify.error(request, 'Invalid form data. Please check the fields and try again.', persistent="Okay")
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/add_announcement.html', {'form': form})

def update_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            try:
                # Save the updated announcement
                form.save()
                
                # Show a success message
                sweetify.success(request, 'Announcement has been updated successfully!', persistent="Okay")
                return redirect('announcement')  # Redirect to the announcements list page
            
            except Exception as e:
                # Log the error (optional)
                print(f"Error updating announcement: {e}")
                
                # Show an error message to the user
                sweetify.error(request, 'An error occurred while updating the announcement. Please try again.', persistent="Okay")
        else:
            # If the form is not valid, show an error message
            sweetify.error(request, 'Invalid form data. Please check the fields and try again.', persistent="Okay")
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'announcements/update_announcement.html', {'form': form, 'announcement': announcement})

def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        try:
            # Delete the announcement
            announcement.delete()
            
            # Show a success message
            sweetify.success(request, 'Announcement has been deleted successfully!', persistent="Okay")
            return redirect('announcement')  # Redirect to the announcements list page
        
        except Exception as e:
            # Log the error (optional)
            print(f"Error deleting announcement: {e}")
            
            # Show an error message to the user
            sweetify.error(request, 'An error occurred while deleting the announcement. Please try again.', persistent="Okay")
    
    return render(request, 'announcements/confirm_delete.html', {'announcement': announcement})


def attendance(request):
    return render(request, 'teacher/attendance.html')

def grades(request):
    return render(request, 'teacher/grades.html')

def ai_recommendation(request):
    return render(request, 'teacher/ai_recommendation.html')
