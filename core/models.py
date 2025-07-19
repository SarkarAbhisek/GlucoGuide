from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(2.5)])  # in meters
    weight = models.FloatField(validators=[MinValueValidator(20), MaxValueValidator(300)])  # in kg
    
    def __str__(self):
        return f"{self.name} (Age: {self.age})"

class BloodTest(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blood_tests')
    fasting_glucose = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    post_prandial_glucose = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    hba1c = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    random_glucose = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blood Test'
        verbose_name_plural = 'Blood Tests'

    def __str__(self):
        return f"Blood Test for {self.user_profile.name} on {self.created_at.date()}"

class RiskAssessment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='risk_assessments')
    physical_activity = models.CharField(max_length=1)
    family_history = models.CharField(max_length=1)
    waist = models.FloatField(validators=[MinValueValidator(50), MaxValueValidator(200)])
    hypertension = models.BooleanField(default=False)
    high_blood_sugar_med = models.BooleanField(default=False)
    fruit_intake = models.BooleanField(default=False)
    high_blood_glucose = models.BooleanField(default=False)
    bmi = models.FloatField(null=True, blank=True)
    idrs_score = models.IntegerField(default=0)
    ada_score = models.IntegerField(default=0)
    findrisc_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Risk Assessment'
        verbose_name_plural = 'Risk Assessments'

    def __str__(self):
        return f"Risk Assessment for {self.user_profile.name} (IDRS: {self.idrs_score})"