# Generated by Django 4.2.13 on 2024-08-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_patient_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
