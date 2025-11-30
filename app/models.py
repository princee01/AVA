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
    course=models.CharField(default='B.Tech')
    dob = models.DateField()
    location = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)

    class Meta:
        unique_together = ('college', 'enroll_no') 

    def __str__(self):
        return f"{self.name} - {self.enroll_no}"  

class Document(models.Model):

    STATUS_CHOICES = (
        ("Uploaded", "Uploaded"),
        ("Verified", "Verified"),
        ("Pending", "Pending"),
        ("Fake", "Fake"),
    )

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

    issued_by_college = models.ForeignKey(
        College,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_documents"
    )

    doc_no = models.CharField(max_length=50)
    doc_id = models.CharField(max_length=100, unique=True)
    document_name = models.CharField(max_length=255)
    issued_to = models.CharField(max_length=255)
    issued_date = models.DateField()
    file = models.FileField(upload_to='documents/')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Uploaded"
    )

    def save(self, *args, **kwargs):

        # 1️⃣ If doc_no matches a college’s pattern → Verified
        if College.objects.filter(college_id=self.doc_no[:4]).exists():
            matched_college = College.objects.get(college_id=self.doc_no[:4])
            self.issued_by_college = matched_college
            self.status = "Verified"

        # 2️⃣ If doc_no prefix not found but format looks valid → Pending verification
        elif self.doc_no.startswith("SIET"):  
            self.status = "Pending"

        # 3️⃣ Document is fake
        else:
            self.status = "Fake"
            self.issued_by_college = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.document_name} ({self.doc_id})"
