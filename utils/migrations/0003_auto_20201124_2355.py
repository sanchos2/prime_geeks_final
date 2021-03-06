# Generated by Django 3.1.3 on 2020-11-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20201124_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='source',
            field=models.TextField(blank=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_left_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Доход мин'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_right_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Доход макс'),
        ),
    ]
