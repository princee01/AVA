from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class College(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     college_name = models.CharField(max_length=255, unique=True, default="Unknown College")
#     college_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
#     college_location = models.CharField(max_length=255, null=True, blank=True)
#     estab_year = models.PositiveIntegerField(null=True, blank=True)
#     college_email = models.EmailField(unique=True, null=True, blank=True)
#     college_photo = models.ImageField(upload_to='college_photos/', null=True, blank=True)
    
#     def __str__(self):
#         return self.college_name if self.college_name else "Unnamed College"

class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Basic info
    college_name = models.CharField(max_length=255, unique=True, default="Unknown College")
    college_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    college_location = models.CharField(max_length=255, null=True, blank=True)
    estab_year = models.PositiveIntegerField(null=True, blank=True)
    college_email = models.EmailField(unique=True, null=True, blank=True)
    college_photo = models.ImageField(upload_to='college_photos/', null=True, blank=True)
    bgimage = models.ImageField(upload_to='college_bg/', null=True, blank=True)

    # Description
    description = models.TextField(null=True, blank=True)

    # Contacts
    contact1 = models.CharField(max_length=20, null=True, blank=True)
    contact2 = models.CharField(max_length=20, null=True, blank=True)
    contact3 = models.CharField(max_length=20, null=True, blank=True)

    # Achievement Section
    Aimage1 = models.ImageField(upload_to='achievements/', null=True, blank=True)
    Atext1 = models.CharField(max_length=255, null=True, blank=True)

    Aimage2 = models.ImageField(upload_to='achievements/', null=True, blank=True)
    Atext2 = models.CharField(max_length=255, null=True, blank=True)

    Aimage3 = models.ImageField(upload_to='achievements/', null=True, blank=True)
    Atext3 = models.CharField(max_length=255, null=True, blank=True)

    # Advantage Section
    Advimage = models.ImageField(upload_to='advantages/', null=True, blank=True)
    Advtext = models.CharField(max_length=255, null=True, blank=True)

    # Awards / Ranking Section
    awardtext = models.CharField(max_length=255, null=True, blank=True)
    p_detail1 = models.CharField(max_length=255, null=True, blank=True)
    p_detail2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.college_name if self.college_name else "Unnamed College"

    
class Student(models.Model):
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="students"
    )

    name = models.CharField(max_length=255)
    enroll_no = models.CharField(max_length=100, unique=True) 
    dob = models.DateField()
    location = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)

    class Meta:
        unique_together = ('college', 'enroll_no') 

    def __str__(self):
        return f"{self.name} - {self.enroll_no}"  

class Document(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    doc_id = models.CharField(max_length=100, unique=True)
    document_name = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)  
    issued_to = models.CharField(max_length=255)      
    issued_date = models.DateField()
    file = models.FileField(upload_to='documents/')

    class Meta:
        unique_together = ('student', 'document_name')
        # ensures no student gets two documents with same name (like 2 marksheet1)

    def __str__(self):
        return f"{self.document_name} ({self.doc_id})"      