# Generated by Django 4.2.3 on 2023-08-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_name', models.CharField(max_length=100)),
            ],
        ),
    ]