# Generated by Django 3.2.12 on 2022-02-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_submission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default='Queued', max_length=50),
        ),
    ]
