from django.http import JsonResponse
from django.shortcuts import render
from .models import Employee, Job, EmployeeSchedule, EmployeeJob
from . import serializers
from rest_framework.decorators import api_view

from .serializers import EmployeeWithAllSchedulesSerializer, EmployeeScheduleSerializer, EmployeeSerializer, \
    JobSerializer


# this Api function contain a combined response for land page.
# but I never used in front-end as I make fetch request from every component.
# and parting it into multiple Api functions.
@api_view(['GET'])
def land_page(request):
    try:
        # get objects for table one.
        employees = Employee.objects.all()
        s_employees = serializers.EmployeeSerializer(instance=employees, many=True)

        # get objects for table two.
        jobs = Job.objects.all()
        s_jobs = serializers.JobSerializer(instance=jobs, many=True)

        # get counts for cards:

        jobs_count = Job.objects.count()
        jobs_without_schedule = Job.objects.filter(status=0).count()
        data = {
            "employees": s_employees.data,
            "jobs": s_jobs.data,
            "jobs_count": jobs_count,
            "jobs_without_schedule": jobs_without_schedule
        }
        return JsonResponse({"ok": True, "message": "done!", "data": data}, safe=False)
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_jobs_count(request):
    try:
        jobs_count = Job.objects.count()
        return JsonResponse({"ok": True, "message": "done!", "data": jobs_count})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_jobs_without_schedules_count(request):
    try:
        jobs_without_schedule = Job.objects.filter(status=0).count()
        return JsonResponse({"ok": True, "message": "done!", "data": jobs_without_schedule})

    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_jobs_all_schedules(request):
    try:
        # get all jobs with every previous schedules.
        jobs = Job.objects.all()
        s_jobs = serializers.JobSerializerAllSchedules(instance=jobs, many=True)

        return JsonResponse({"ok": True, "message": "done!", "data": s_jobs.data}, safe=False)
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_jobs_with_active_schedules(request):
    try:
        # get all jobs and only active schedules(haven't employees or have employee working on it).
        # this filtering only on schedules
        jobs = Job.objects.all()
        s_jobs = serializers.JobSerializer(instance=jobs, many=True)

        return JsonResponse({"ok": True, "message": "done!", "data": s_jobs.data}, safe=False)
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_specific_job(request, job_id):
    try:
        # get job then serialize it with all schedules.
        job = Job.objects.get(id=job_id)
        s_job = serializers.JobSerializerAllSchedules(instance=job)
        return JsonResponse({"ok": True, "message": "done!", "data": s_job.data})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(['GET'])
def get_employees(request):
    try:
        employees = Employee.objects.all()
        s_employees = serializers.EmployeeWithAllSchedulesSerializer(instance=employees, many=True)
        return JsonResponse({"ok": True, "message": "done!", "data": s_employees.data})

    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["GET"])
def get_available_employees_in_specific_period(request):
    try:
        # get the start-date and end-date from request body.
        start = request.data['start']
        end = request.data['end']
        # query to get available employees:
        av_employees = Employee.objects.filter(employeeschedule__status=0, employeeschedule__start_at__gte=start,
                                               employeeschedule__end_at__lte=end)
        print()
        s_employees = EmployeeWithAllSchedulesSerializer(instance=av_employees, many=True)
        print(s_employees)
        return JsonResponse({'ok': True, "message": "done!", "data": s_employees.data})
    except KeyError:
        return JsonResponse({'ok': False, "message": "make sure that keys is: start, end.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["GET"])
def get_available_employees_count_in_specific_period(request):
    try:
        # get the start-date and end-date from request body.
        start = request.data['start']
        end = request.data['end']
        # query to get available employees:
        av_employees_count = Employee.objects.filter(employeeschedule__status=0, employeeschedule__start_at__gte=start,
                                                     employeeschedule__end_at__lte=end).count()
        response_data = {
            'count': av_employees_count
        }
        return JsonResponse({'ok': True, "message": "done!", "data": response_data})
    except KeyError:
        return JsonResponse({'ok': False, "message": "make sure that keys is: start, end.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["POST"])
def add_schedule_to_employee(request):
    try:
        # the body must have a keys:
        # employee_id, start_at, end_at
        st = request.data['start_at']
        en = request.data['end_at']
        employee_id = request.data['employee_id']
        # search for employee id.
        employee = Employee.objects.get(id=employee_id)
        # we can add constrain to restrict adding more than one schedule at the same period.
        # create relation.
        employee_s = EmployeeSchedule(employee=employee, start_at=st, end_at=en, status=0)
        employee_s.save()
        return JsonResponse({'ok': True, "message": "Added!", "data": None})
    except KeyError:
        return JsonResponse(
            {'ok': False, "message": "make sure that keys is: employee_id, start_at, end_at.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["POST"])
def add_employee(request):
    try:
        # creating employee using serializer.
        # make sure that keys is: first_name, last_name, birth_date.
        employee = EmployeeSerializer(data=request.data)
        if employee.is_valid():
            employee.save()
            return JsonResponse({'ok': True, "message": "Added!", "data": None})
        return JsonResponse({'ok': False, "message": "not valid data!", "data": None})
    except KeyError:
        return JsonResponse(
            {'ok': False, "message": "make sure that keys is: first_name, last_name, birth_date.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["POST"])
def add_job(request):
    try:
        data = request.data
        data['status'] = 0
        job = JobSerializer(data=request.data)

        if job.is_valid():
            job.save()
            return JsonResponse({'ok': True, "message": "Added!", "data": None})
        return JsonResponse({'ok': False, "message": "not valid data!", "data": None})

    except KeyError:
        return JsonResponse(
            {'ok': False, "message": "make sure that keys is: name, description, start_at, end_at.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})


@api_view(["POST"])
def select_employee_for_job(request):
    try:
        em_id = request.data['employee_id']
        jb_id = request.data['job_id']
        tk_date = request.data['taken_date']

        job = Job.objects.get(id=jb_id)
        # we can add constrain for restricting the conflicts.
        employee_job = EmployeeJob(employee_id=em_id, job=job, taken_date=tk_date, status=0)
        employee_job.save()

        # update job status
        job.status = 1
        job.save()
        return JsonResponse({'ok': True, "message": "Added!", "data": None})
    except KeyError:
        return JsonResponse(
            {'ok': False, "message": "make sure that keys is: employee_id, job_id, taken_date.", "data": None})
    except Exception as ex:
        print(ex)
        return JsonResponse({'ok': False, "message": "some error happen!", "data": None})
