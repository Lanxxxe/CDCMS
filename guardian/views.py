from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'guardian_dashboard.html')

def announcement(request):
    return render(request, 'guardian/announcement.html')