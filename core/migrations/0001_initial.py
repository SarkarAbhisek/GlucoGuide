# Generated by Django 5.1.2 on 2025-07-16 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")], max_length=10
                    ),
                ),
                ("height", models.FloatField()),
                ("weight", models.FloatField()),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RiskAssessment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("physical_activity", models.CharField(max_length=1)),
                ("family_history", models.CharField(max_length=1)),
                ("waist", models.FloatField()),
                ("hypertension", models.BooleanField()),
                ("high_blood_sugar_med", models.BooleanField()),
                ("fruit_intake", models.BooleanField()),
                ("high_blood_glucose", models.BooleanField()),
                ("bmi", models.FloatField()),
                ("idrs_score", models.IntegerField()),
                ("ada_score", models.IntegerField()),
                ("findrisc_score", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.userprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BloodTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fasting_glucose", models.FloatField(blank=True, null=True)),
                ("post_prandial_glucose", models.FloatField(blank=True, null=True)),
                ("hba1c", models.FloatField(blank=True, null=True)),
                ("random_glucose", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.userprofile",
                    ),
                ),
            ],
        ),
    ]
