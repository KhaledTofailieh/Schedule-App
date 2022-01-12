from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=True, default='')
    birth_date = models.DateField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


# --------------------------------------------------------------------------------


# this is One-to-Many relation between employee and schedule
# so by this relation, the employee can has many schedules
# we can add a constrain in server for restricting the schedules conflict.
class EmployeeSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_at = models.DateField(null=False)
    end_at = models.DateField(null=False)
    status = models.IntegerField(default=0)

    # the status values can be:
    # 0: if the schedule still active(employee is available)
    # 1: if the employee take a job in this schedule(is not available to take any job)
    # -1: if the schedule is expired.

    def __str__(self):
        return "{} | {}".format(self.employee.__str__(), self.start_at)

    # I can deal with job-Schedule in the same way I deal with Employee-Schedule


# but at this moment I prefer to keep it simple.
# --------------------------------------------------------------------------------

class Job(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)
    start_at = models.DateField(null=False)
    end_at = models.DateField(null=False)
    status = models.IntegerField(default=0)
    # the status field show as values:
    # 0: the job haven't any employee(one employee at least in my case).
    # 1: the job is taken by an employee(one employee at least in my case).
    # -1: the job schedule has expired.

    employees = models.ManyToManyField(Employee, through='EmployeeJob', related_name='job_employees')

    # so through this relation we can fetch all the employees of this Jop, we can filter it as the requirements need.
    def __str__(self):
        return "{} | {}".format(self.name, self.start_at)


# -----------------------------------------------------------------------------------

# this is Many-to_Many relation between employee and job.
# so by this, I give the system some dynamically use.
class EmployeeJob(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    taken_date = models.DateField()
    status = models.IntegerField(null=True, default=0)

    # the status field can take values as following:
    # 0: if the employee still working in that job
    # 1: if the employee done it.
    # -1: if the employee draft his job and didn't complete it.
    def __str__(self):
        return "{} | {}".format(self.employee.__str__(), self.job)
# --------------------------------------------------------------------------------
