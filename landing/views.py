from django.shortcuts import render, redirect
from .forms import EnrollmentForm
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'landing/about.html')

def enroll(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            # Process form data (e.g., save to database, send email, etc.)
            print(form.cleaned_data)  # Debugging: Check the submitted data
            return redirect('enrollment_success')  # Redirect to a success page
    else:
        form = EnrollmentForm()
    
    return render(request, 'enrollment.html', {'form': form})