from rest_framework import serializers
from .models import EmployeeJob, Employee, EmployeeSchedule, Job


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'birth_date']


# ---------------------------------------------------------------------------------------

# the EmployeeJobSerializer is to serialize the Many-to-Many relation between employee and schedule and get relation fields.
class EmployeeJobSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = EmployeeJob
        fields = ['id', 'status', 'taken_date', 'employee']


# the JobSerializer is to serialize Jobs with filtering schedules(getting only active schedules)
# that filtering because of my database designing that say: the Job may have multiple employees.
class JobSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField(source='get_schedules', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'name', 'status', 'start_at', 'end_at', 'schedules']

    def get_schedules(self, instance):
        active_employee_job = instance.employeejob_set.filter(status=0)
        return EmployeeJobSerializer(active_employee_job, read_only=True, many=True).data


# the JobSerializer is to serialize Jobs without filtering schedules(getting only active schedules)
# to get (expired, drafted and active) schedules
class JobSerializerAllSchedules(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField(source='get_schedules', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'name', 'schedules']

    def get_schedules(self, instance):
        active_employee_job = instance.employeejob_set
        return EmployeeJobSerializer(active_employee_job, read_only=True, many=True).data


# ---------------------------------------------------------------------------------------------

#  this below two classes for API of:
# get available employees in specific date.
# but here I want to show all information in addition to counts.
class EmployeeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        # EmployeeSchedule: is One-to-Many relation
        model = EmployeeSchedule
        fields = ['id', 'start_at', 'end_at', 'status']


class EmployeeWithAllSchedulesSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField(source='get_schedules', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'schedules']

    def get_schedules(self, instance):
        active_employee_schedules = instance.employeeschedule_set
        return EmployeeScheduleSerializer(active_employee_schedules, read_only=True, many=True).data
