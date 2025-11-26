from django.contrib import admin
from .models import College, Student, Document

# Register your models here.
admin.site.register(College)
admin.site.register(Student)
admin.site.register(Document)