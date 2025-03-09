from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from teacher.views import *

urlpatterns = [
    path('', dashboard, name='teacher_dashboard'),
    path('student-management/', student_management, name='student_management'),
    path('profile/', profile, name='teacher_profile'),
    
    # Guardians
    path('guardian-management/', guardian_management, name='guardian_management'),
    path('guardians/update/<int:id>/', update_guardian, name='update_guardian'),
    
    # Teachers
    path('teacher-management/', teacher_management, name='teacher_management'),
    
    # Announcements
    path('announcement/', announcement, name='announcement'),
    path('announcements/add/', add_announcement, name='add_announcement'),
    path('announcements/update/<int:id>/', update_announcement, name='update_announcement'),
    path('announcements/delete/<int:id>/', delete_announcement, name='delete_announcement'),
    
    # Attendance
    path('attendance/', attendance, name='attendance'),
    path('change_attendance/', change_attendance, name='change_attendance'),    
    
    # Grades
    path('grades/', grades, name='grades'),
    path('grades/<str:student_id>/', view_student_grades, name='view_student_grades'),
    path('grades/update/<str:student_id>/', update_student_grades, name='update_student_grades'),
    
    # AI
    path('ai_recommendation/', ai_recommendation, name='ai_recommendation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)