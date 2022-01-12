from django.contrib import admin
from .models import Employee, EmployeeJob, EmployeeSchedule, Job
# Register your models here.
admin.site.register(Employee)
admin.site.register(EmployeeJob)
admin.site.register(EmployeeSchedule)
admin.site.register(Job)

