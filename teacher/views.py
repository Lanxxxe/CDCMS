from django.core.paginator import Paginator
from django.utils.timezone import localdate
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, CharField, F, Q
from django.db.models.functions import Concat
from django.http import JsonResponse
from landing.models import Student, GuardianInfo, Enrollment, Announcement, Attendance, StudentEvaluation, StandardScore, Recommendation
from datetime import date, datetime
from .forms import AnnouncementForm, GuardianInfoForm, StudentEvaluationForm
from .utils import mask_email, get_suggestion
import sweetify, json

def main(request):
    return render(request, 'old.html')

def dashboard(request):
    student_count = Student.objects.count()
    guardian_count = GuardianInfo.objects.count()
    enrollments = Enrollment.objects.all()
    today_attendance = Attendance.objects.filter(date=localdate())

    complete_count = 0
    incomplete_count = 0

    for enrollment in enrollments:
        if enrollment.psa and enrollment.guardianQCID and enrollment.recentPhoto and enrollment.immunizationCard:
            complete_count += 1
        else:
            incomplete_count += 1



    data = {
        'student_count' : student_count,
        'guardian_count' : guardian_count,
        'complete_count': complete_count,
        'incomplete_count': incomplete_count,
        'total_students' : today_attendance.count(),
        'present_count' : today_attendance.filter(status="Present").count(),
        'absent_count' : today_attendance.filter(status="Absent").count()
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
    return render(request, 'teacher/student_management.html', context)

def guardian_management(request):
    guardians = GuardianInfo.objects.select_related('student').all()

    for guardian in guardians:
        guardian.email = mask_email(guardian.email)

    data = {
        'guardians': guardians,
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
                sweetify.error(request, f'An error occurred while updating the guardian information: {form.errors}', persistent="Okay")
        else:
            # If the form is not valid, show an error message
            print(form.errors)
            sweetify.error(request, f'Invalid form data. Please check the fields and try again.', persistent="Okay")
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
    selected_date = request.GET.get('date', date.today())  # Get date from the request or use today

    students = Student.objects.all()
    student_data = []

    for student in students:
        # Fetch the latest attendance for the selected date
        attendance = Attendance.objects.filter(student=student, date=selected_date).first()
        status = attendance.status if attendance else "No Record"

        student_data.append({
            'id': student.id,
            'student_id': student.student_id,
            'firstName': student.firstName,
            'lastName': student.lastName,
            'status': status
        })
    return render(request, 'teacher/attendance.html', {'students': student_data, 'selected_date': selected_date})

def change_attendance(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        selected_date = request.POST.get('date')

        # Validate date format
        try:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'})

        student = get_object_or_404(Student, id=student_id)

        # ✅ Update or create the attendance record
        attendance, created = Attendance.objects.update_or_create(
            student=student,
            date=selected_date,
            defaults={'status': status}
        )

        return JsonResponse({'success': True, 'status': status, 'updated': not created})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def grades(request):
    kinder_level = request.GET.get('kinder_level', '')  # Get filter value

    # Fetch students with their enrollment and evaluation data
    students = Student.objects.prefetch_related('enrollment', 'evaluations')

    if kinder_level:
        students = students.filter(enrollment__schedule=kinder_level)

    # Sort students by Kinder Level ('K1', 'K2', etc.)
    students = students.order_by('enrollment__schedule')

    # Prepare evaluation data for each student
    student_data = []
    for student in students:
        first_eval = student.evaluations.filter(evaluation_period='First').first()
        second_eval = student.evaluations.filter(evaluation_period='Second').first()

        # Calculate total scores
        first_total = (
            first_eval.gross_motor_score + first_eval.fine_motor_score +
            first_eval.self_help_score + first_eval.receptive_language_score +
            first_eval.expressive_language_score + first_eval.cognitive_score +
            first_eval.socio_emotional_score
        ) if first_eval else None

        second_total = (
            second_eval.gross_motor_score + second_eval.fine_motor_score +
            second_eval.self_help_score + second_eval.receptive_language_score +
            second_eval.expressive_language_score + second_eval.cognitive_score +
            second_eval.socio_emotional_score
        ) if second_eval else None

        student_data.append({
            'student': student,
            'first_total': first_total,
            'second_total': second_total,
        })

    # Pagination (10 students per page)
    paginator = Paginator(student_data, 10)
    page_number = request.GET.get('page')
    page_students = paginator.get_page(page_number)

    # Get unique kinder levels for the filter dropdown
    kinder_levels = Enrollment.objects.values_list('schedule', flat=True).distinct()

    context = {
        'students': page_students,
        'kinder_levels': kinder_levels,
        'selected_level': kinder_level
    }

    return render(request, 'teacher/grades.html', context)

def view_student_grades(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    evaluations = StudentEvaluation.objects.filter(student=student)
    print(evaluations)
    context = {
        'student': student,
        'evaluations': evaluations
    }
    return render(request, 'grades/view_grades.html', context)


def update_student_grades(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    evaluation_period = request.GET.get('evaluation_period')

    if request.method == "POST":
        evaluation_period = request.POST.get('evaluation_period')
        evaluation, created = StudentEvaluation.objects.get_or_create(
            student=student,
            evaluation_period=evaluation_period,
        )
        form = StudentEvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluation_period = evaluation_period
            evaluation.save()

             # Fetch standard scores for the selected semester
            try:
                standard_scores = StandardScore.objects.get(semester=evaluation_period)
            except StandardScore.DoesNotExist:
                standard_scores = None

            # Construct the JSON object
            student_performance = {
                "name": f"{student.firstName} {student.lastName}",
                "semester": evaluation_period,
                "student_grades": {
                    "Gross Motor": evaluation.gross_motor_score,
                    "Fine Motor": evaluation.fine_motor_score,
                    "Self Help": evaluation.self_help_score,
                    "Receptive Language": evaluation.receptive_language_score,
                    "Expressive Language": evaluation.expressive_language_score,
                    "Cognitive": evaluation.cognitive_score,
                    "Socio-Emotional": evaluation.socio_emotional_score,
                },
                "standard_raw_scores": {
                    "Gross Motor": standard_scores.gross_motor if standard_scores else 0,
                    "Fine Motor": standard_scores.fine_motor if standard_scores else 0,
                    "Self Help": standard_scores.self_help if standard_scores else 0,
                    "Receptive Language": standard_scores.receptive_language if standard_scores else 0,
                    "Expressive Language": standard_scores.expressive_language if standard_scores else 0,
                    "Cognitive": standard_scores.cognitive if standard_scores else 0,
                    "Socio-Emotional": standard_scores.socio_emotional if standard_scores else 0,
                }
            }

            recommendation, created = Recommendation.objects.get_or_create(
                student=student,
                evaluation_period=evaluation_period,
                defaults={'recommendation': get_suggestion(student_data=student_performance)}  # Set the recommendation if creating a new record
            )

            if not created:
                recommendation.recommendation = get_suggestion(student_data=student_performance)
                recommendation.save()

            sweetify.toast(request, "Updated Successfully", icon="success", timer=3000)
            return redirect('grades')
    else:
        if evaluation_period:
            evaluation = StudentEvaluation.objects.filter(
                student=student,
                evaluation_period=evaluation_period,
            ).first()
            form = StudentEvaluationForm(instance=evaluation)
        else:
            form = None

    context = {
        'student': student,
        'form': form,
        'evaluation_period': evaluation_period,
    }
    return render(request, 'grades/update_grades.html', context)


def ai_recommendation(request):
    # Get filter parameters from the request
    kinder_level = request.GET.get('kinder_level', '')  # Default to empty string (all levels)

    # Fetch all students
    students = Student.objects.all()

    # Apply filters if provided
    if kinder_level:
        students = students.filter(enrollment__schedule=kinder_level)

    # Prepare data for the template
    student_data = []
    for student in students:
        # Get recommendations for both evaluation periods
        first_recommendation = student.recommendations.filter(evaluation_period='First').first()
        second_recommendation = student.recommendations.filter(evaluation_period='Second').first()

        student_data.append({
            'student_id': student.student_id,
            'kinder_level': student.enrollment.first().schedule if student.enrollment.exists() else '-',
            'full_name': f"{student.firstName} {student.lastName}",
            'first_recommendation': first_recommendation.recommendation if first_recommendation else '-',
            'second_recommendation': second_recommendation.recommendation if second_recommendation else '-',
        })

    # Pagination (10 students per page)
    paginator = Paginator(student_data, 10)
    page_number = request.GET.get('page')
    page_students = paginator.get_page(page_number)

    # Get unique Kinder Levels for the filter dropdown (Kinder 1 to Kinder 3)
    kinder_levels = ['Kinder 1', 'Kinder 2', 'Kinder 3']

    context = {
        'page_students': page_students,
        'kinder_levels': kinder_levels,
        'selected_kinder_level': kinder_level,

    }

    return render(request, 'teacher/ai_recommendation.html', context)
