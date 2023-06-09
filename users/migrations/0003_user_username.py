# Generated by Django 4.2.2 on 2023-06-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                unique=True,
                verbose_name="Username",
            ),
        ),
    ]
