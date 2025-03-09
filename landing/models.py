from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
import re, uuid, os

def secure_file_path(instance, filename):
    student_name = f"{instance.student.firstName}_{instance.student.lastName}".replace(" ", "_")
    requirement = instance._meta.get_field(instance._meta.get_fields()[-1].name).name  # Gets the last field
    
    ext = filename.split('.')[-1]
    unique_filename = f"{student_name}_{requirement}.{ext}"
    
    return os.path.join('secure_files', student_name, requirement, unique_filename)     

def validate_ph_contact(value):
    """ Ensure number starts with '09' and has exactly 11 digits. """
    pattern = r"^09\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 11-digit Philippine mobile number starting with 09.")
    

class Student(models.Model):
    id = models.AutoField(primary_key=True)  # Matches MySQL schema
    student_id = models.CharField(max_length=20, unique=True)
    firstName = models.CharField(max_length=50, blank=False, null=False)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    healthHistory = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student'


class StudentAddress(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")  # ForeignKey match
    address_no = models.CharField(max_length=100, blank=False, null=False)
    baranggay = models.CharField(max_length=100, blank=False, null=False)
    municipality = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'student_address'


class FatherInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50, blank=False, null=False)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    contact_number = models.CharField(max_length=15, validators=[MinLengthValidator(11)])

    class Meta:
        db_table = 'father_info'


class MotherInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50, blank=False, null=False)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    contact_number = models.CharField(max_length=15, validators=[MinLengthValidator(11)])

    class Meta:
        db_table = 'mother_info'


class GuardianInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50, blank=False, null=False)
    middleName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    relationship = models.CharField(max_length=50, blank=False, null=False)
    contact_number = models.CharField(max_length=15, validators=[MinLengthValidator(11)], blank=False, null=True)
    email = models.EmailField(blank=False, null=False)
    occupation = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'guardian_info'


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="student_id", related_name="enrollment")
    schedule = models.TextField()
    psa = models.ImageField(upload_to=secure_file_path)
    immunizationCard = models.ImageField(upload_to=secure_file_path, blank=True, null=True)
    recentPhoto = models.ImageField(upload_to=secure_file_path, blank=True, null=True)
    guardianQCID = models.ImageField(upload_to=secure_file_path)

    class Meta:
        db_table = 'enrollment'


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    posted_by = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='announcements/images/', blank=False, null=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'announcement'


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="student_id")
    date = models.DateField()  # Ensures each entry has a date
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'attendance'
        unique_together = ('student', 'date')


class StudentEvaluation(models.Model):
    EVALUATION_PERIOD_CHOICES = [
        ('First', 'First Evaluation'),
        ('Second', 'Second Evaluation'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="evaluations")
    evaluation_period = models.CharField(max_length=10, choices=EVALUATION_PERIOD_CHOICES)  # Match ENUM values!

    gross_motor_score = models.IntegerField()
    fine_motor_score = models.IntegerField()
    self_help_score = models.IntegerField()
    receptive_language_score = models.IntegerField()
    expressive_language_score = models.IntegerField()
    cognitive_score = models.IntegerField()
    socio_emotional_score = models.IntegerField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_evaluation'
        unique_together = ('student', 'evaluation_period')

 
class Recommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='recommendations')
    evaluation_period = models.CharField(max_length=20)
    recommendation = models.TextField()

    class Meta:
        db_table = 'recommendation' 
        unique_together = ('student', 'evaluation_period')

class StandardScore(models.Model):
    SEMESTER_CHOICES = [
        ('First', 'First Semester'),
        ('Second', 'Second Semester'),
    ]

    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, unique=True)

    gross_motor = models.IntegerField()
    fine_motor = models.IntegerField()
    self_help = models.IntegerField()
    receptive_language = models.IntegerField()
    expressive_language = models.IntegerField()
    cognitive = models.IntegerField()
    socio_emotional = models.IntegerField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'standard_scores'

    def __str__(self):
        return f"Standard Scores - {self.semester}"



