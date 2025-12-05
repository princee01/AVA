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
        ("Issued", "Issued"),  # Added Issued status
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
    doc_id = models.CharField(max_length=100)
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
    # Clean doc_no
        self.doc_no = self.doc_no.strip().upper()
        prefix = self.doc_no[:4]

    # Only override status if it's not manually set to something meaningful
        if self.status in ["Uploaded", None, ""]:
        
        # Manually typed issuing college (coming from view)
           issuing_college = self.issued_by_college

        # Check if student exists
           student_exists = Student.objects.filter(id=self.student_id).exists()

        # Check existing document by doc_no (NOT doc_id)
           existing_doc = Document.objects.filter(doc_no=self.doc_no).exclude(id=self.id).first()

        # Case 1: doc_no already exists → Verified
           if existing_doc and student_exists:
            self.status = "Verified"
            self.issued_by_college = existing_doc.issued_by_college

        # Case 2: issued_by exists but doc_no does not match → Pending
           elif issuing_college and student_exists:
            self.status = "Pending"

        # Case 3: issued_by college does NOT exist → Fake
           else:
            self.status = "Fake"
            self.issued_by_college = None

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.document_name} ({self.doc_id})"
