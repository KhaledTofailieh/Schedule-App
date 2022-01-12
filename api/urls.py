from django.urls import path
from . import views

urlpatterns = [
    path('', views.land_page),

    path('employees', views.get_employees),
    path('available-employees', views.get_available_employees_in_specific_period),
    path('available-employees-count', views.get_available_employees_count_in_specific_period),

    path('jobs', views.get_jobs_all_schedules),
    path('jobs-count', views.get_jobs_count),
    path('jobs-count-without-schedules', views.get_jobs_without_schedules_count),
    path('active-jobs', views.get_jobs_with_active_schedules),
    path('jobs/<job_id>', views.get_specific_job),
    path('job', views.add_job),

    path('employee-schedule', views.add_schedule_to_employee),
    path('employee-job', views.select_employee_for_job),
    path('employee', views.add_employee),
]
