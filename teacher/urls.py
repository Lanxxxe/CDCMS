from django.urls import path, include
from teacher.views import *

urlpatterns = [
    path('', dashboard, name='teacher_dashboard'),
    path('student-management/', student_management, name='student_management'),
    path('guardian-management/', guardian_management, name='guardian_management'),
    path('teacher-management/', teacher_management, name='teacher_management'),
    path('announcement/', announcement, name='announcement'),
    path('attendance/', attendance, name='attendance'),
    path('grades/', grades, name='grades'),
    path('ai_recommendation/', ai_recommendation, name='ai_recommendation'),
]
