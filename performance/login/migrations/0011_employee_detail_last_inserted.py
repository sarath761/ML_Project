# Generated by Django 4.2.3 on 2023-08-12 08:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_delete_uploadedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_detail',
            name='last_inserted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
