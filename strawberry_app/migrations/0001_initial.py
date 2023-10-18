# Generated by Django 4.1.7 on 2023-04-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Culture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="Months",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=15)),
                ("cult", models.ManyToManyField(to="strawberry_app.culture")),
            ],
        ),
    ]
