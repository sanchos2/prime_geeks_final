# Generated by Django 3.1.3 on 2020-11-24 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20201124_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='source_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ID вакансии'),
        ),
    ]
