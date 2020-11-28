from django.db import models


class Candidate(models.Model):
    gender = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(blank=True)
    city = models.CharField(max_length=200, blank=True)
    ready_to_move = models.TextField(blank=True)
    title = models.TextField()
    salary = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    branch = models.TextField(blank=True)
    spec = models.TextField(blank=True)
    type_of_work = models.TextField(blank=True)
    work_schedule = models.TextField(blank=True)
    total_work_exp = models.PositiveIntegerField(null=True, blank=True)
    last_employee = models.TextField(blank=True)
    last_job_title = models.TextField(blank=True)
    last_job_responsibilities = models.TextField(blank=True)
    last_job_time = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(blank=True)
    about_candidate = models.TextField(blank=True)
    education = models.TextField(blank=True)
    source = models.TextField(blank=True)
    source_id = models.CharField(max_length=200, blank=True)


class Language(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='languages',
    )
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=200)


