# Generated by Django 2.1.11 on 2020-05-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0004_auto_20200508_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uprofile',
            name='birthday',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
