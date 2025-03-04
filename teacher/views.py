from django.shortcuts import render

def dashboard(request):
    return render(request, 'teacher_dashboard.html')


def student_management(request):
    return render(request, 'teacher/student_management.html')

def guardian_management(request):
    return render(request, 'teacher/guardian_management.html')

def teacher_management(request):
    return render(request, 'teacher/teacher_management.html')

def announcement(request):
    return render(request, 'teacher/announcement.html')

def attendance(request):
    return render(request, 'teacher/attendance.html')

def grades(request):
    return render(request, 'teacher/grades.html')

def ai_recommendation(request):
    return render(request, 'teacher/ai_recommendation.html')
