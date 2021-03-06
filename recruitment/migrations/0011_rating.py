# Generated by Django 3.1.3 on 2020-11-29 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0010_auto_20201129_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ratings', serialize=False, to='recruitment.candidate')),
                ('skill', models.IntegerField(blank=True, null=True, verbose_name='Рейтинг навыков')),
                ('social', models.IntegerField(blank=True, null=True, verbose_name='Социальный рейтинг')),
            ],
            options={
                'ordering': ['skill'],
            },
        ),
    ]
