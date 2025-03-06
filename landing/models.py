from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
import re, uuid, os

def secure_file_path(instance, filename):
    student_name = f"{instance.student.firstName}_{instance.student.lastName}".replace(" ", "_")
    # Generate a UUID for the folder name
    folder_name = uuid.uuid4().hex
    # Generate a UUID for the filename
    ext = filename.split('.')[-1]
    filename = f"{student_name}{uuid.uuid4().hex}.{ext}"
    # Create a path with multiple nested folders
    return os.path.join('secure_files', folder_name[:4], student_name, filename)


def validate_ph_contact(value):
    """ Ensure number starts with '09' and has exactly 11 digits. """
    pattern = r"^09\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 11-digit Philippine mobile number starting with 09.")
    

class Student(models.Model):
    id = models.AutoField(primary_key=True)  # Matches MySQL schema
    student_id = models.CharField(max_length=20, unique=True)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
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
    address_no = models.CharField(max_length=100)
    baranggay = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)

    class Meta:
        db_table = 'student_address'


class FatherInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    contact_number = models.BigIntegerField(validators=[MinLengthValidator(11)])

    class Meta:
        db_table = 'father_info'


class MotherInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    contact_number = models.BigIntegerField(validators=[MinLengthValidator(11)])

    class Meta:
        db_table = 'mother_info'


class GuardianInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, db_column="student_id")
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50)
    contact_number = models.BigIntegerField(validators=[MinLengthValidator(11)])
    email = models.EmailField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'guardian_info'


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column="student_id")
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
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'attendance'
