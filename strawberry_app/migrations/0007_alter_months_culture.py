# Generated by Django 4.1.7 on 2023-05-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strawberry_app', '0006_rename_name_culture_culture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='months',
            name='culture',
            field=models.ManyToManyField(related_name='months', to='strawberry_app.culture'),
        ),
    ]
