# Generated by Django 3.1.4 on 2020-12-26 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201226_2006'),
        ('jobs', '0003_auto_20201226_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantsjobmap',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.applicant'),
        ),
    ]
