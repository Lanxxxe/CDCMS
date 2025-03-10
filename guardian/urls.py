from django.urls import path
from guardian.views import *

urlpatterns = [
    path('', announcement, name='guardian_announcement'),
    path('attendance', attendance, name='guardian_attendance'),
    path('grades', grades, name='guardian_grades'),
    path('requirements', requirements, name='guardian_requirements'),
    path('requirements/<int:student_id>/<str:requirement>/', add_or_update_requirement, name="add_requirement"),
    path('teachers_profile', teachers_profile, name='guardian_teachers_profile'),
    path('ai_recommendation', ai_recommendation, name='guardian_ai_recommendation'),
]
