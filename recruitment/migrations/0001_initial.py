# Generated by Django 3.1.3 on 2020-11-28 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=200)),
                ('age', models.PositiveIntegerField(blank=True)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('ready_to_move', models.TextField(blank=True)),
                ('title', models.TextField()),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('branch', models.TextField(blank=True)),
                ('spec', models.TextField(blank=True)),
                ('type_of_work', models.TextField(blank=True)),
                ('work_shedule', models.TextField(blank=True)),
                ('total_work_exp', models.DateTimeField(blank=True, null=True)),
                ('last_employee', models.TextField(blank=True)),
                ('last_job_title', models.TextField(blank=True)),
                ('last_job_responsibilities', models.TextField(blank=True)),
                ('last_job_time', models.DateTimeField(blank=True, null=True)),
                ('skills', models.TextField(blank=True)),
                ('about_candidate', models.TextField(blank=True)),
                ('education', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.CharField(max_length=200)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='recruitment.candidate')),
            ],
        ),
    ]
