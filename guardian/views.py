from django.shortcuts import render


def announcement(request):
    return render(request, 'guardian/announcement.html')

def attendance(request):
    return render(request, 'guardian/attendance.html')

def grades(request):
    return render(request, 'guardian/grades.html')

def requirements(request):
    return render(request, 'guardian/requirements.html')

def teachers_profile(request):
    return render(request, 'guardian/teachers_profile.html')

def ai_recommendation(request):
    return render(request, 'guardian/ai_recommendation.html')