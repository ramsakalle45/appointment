# Generated by Django 4.2.13 on 2024-08-12 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_patient_mobile_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(blank=True, max_length=12, null=True)),
                ('reports', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
