# Generated by Django 5.1.1 on 2024-10-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_hospitalclinic_remove_doctorprofile_clinic_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='doctorverification',
            name='license_document',
            field=models.FileField(upload_to='media/doctor_licenses/'),
        ),
        migrations.AlterField(
            model_name='hospitalclinic',
            name='hospital_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/hospital_pictures/'),
        ),
        migrations.AlterField(
            model_name='hospitalimage',
            name='image',
            field=models.ImageField(upload_to='media/hospital_images/'),
        ),
    ]
