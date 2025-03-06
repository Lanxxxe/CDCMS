from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now, timedelta
from django.db.models import Q
from landing.models import Announcement, Attendance, Student, Enrollment
import sweetify


def announcement(request):
    announcements = Announcement.objects.all().order_by('-date_posted').values(
    'id', 'posted_by', 'title', 'picture', 'upload_date', 'description', 'date_posted'
    )
    context = {
        'announcements' : announcements
    }
    return render(request, 'guardian/announcement.html', context)

def attendance(request):
    # Convert to lowercase for case-insensitive comparison
    guardian_firstname = 'test'
    guardian_middlename = 'test'
    guardian_lastname = 'test'

    # Get the start of the week (Monday)
    start_of_week = now().date() - timedelta(days=now().weekday())
    
    # Filter the student based on Guardian's name
    students = Student.objects.filter(
        guardianinfo__firstName__iexact=guardian_firstname,
        guardianinfo__middleName__iexact=guardian_middlename,
        guardianinfo__lastName__iexact=guardian_lastname
    )

    # Get attendance records for this week
    attendance_records = Attendance.objects.filter(
        student__in=students,
        date__gte=start_of_week  # Attendance from start of the week till today
    ).values(
        'student__student_id', 
        'student__firstName', 
        'student__middleName', 
        'student__lastName', 
        'date', 
        'status'
    ).order_by('-date')  # Latest first

    context = {'attendance_records': attendance_records}
    return render(request, 'guardian/attendance.html', context)

def grades(request):
    return render(request, 'guardian/grades.html')

def requirements(request):
    enrollment = get_object_or_404(Enrollment, student__id=4)
    
    requirements = {
        "psa": enrollment.psa,
        "immunizationCard": enrollment.immunizationCard,
        "recentPhoto": enrollment.recentPhoto,
        "guardianQCID": enrollment.guardianQCID,
    }

    context = {
        "requirements": requirements,
        "student_id": enrollment.student.id  # ✅ Pass student_id to template
    }

    return render(request, 'guardian/requirements.html', context)


def add_or_update_requirement(request, student_id, requirement):
    enrollment = get_object_or_404(Enrollment, student__id=student_id)
    print(enrollment)
    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            setattr(enrollment, requirement, file)  # Dynamically set the field
            enrollment.save()
            sweetify.success(request, f"{requirement.replace('_', ' ').title()} uploaded successfully!")
            return redirect("guardian_requirements", student_id=student_id)

    return render(request, "requirements/requirement_form.html", {"requirement_name": requirement})


def teachers_profile(request):
    return render(request, 'guardian/teachers_profile.html')

def ai_recommendation(request):
    return render(request, 'guardian/ai_recommendation.html')