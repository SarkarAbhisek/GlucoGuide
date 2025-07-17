from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField()  # in meters
    weight = models.FloatField()  # in kg
    
    def __str__(self):
        return self.name

class BloodTest(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fasting_glucose = models.FloatField(null=True, blank=True)
    post_prandial_glucose = models.FloatField(null=True, blank=True)
    hba1c = models.FloatField(null=True, blank=True)
    random_glucose = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RiskAssessment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    physical_activity = models.CharField(max_length=1)
    family_history = models.CharField(max_length=1)
    waist = models.FloatField()
    hypertension = models.BooleanField()
    high_blood_sugar_med = models.BooleanField()
    fruit_intake = models.BooleanField()
    high_blood_glucose = models.BooleanField()
    bmi = models.FloatField()
    idrs_score = models.IntegerField()
    ada_score = models.IntegerField()
    findrisc_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_physical_activity_display(self):
        return {
            'a': 'Exercise (regular) + strenuous work',
            'b': 'Exercise (regular) or strenuous work',
            'c': 'No Exercise or strenuous work',
        }.get(self.physical_activity, '')

    def get_family_history_display(self):
        return {
            'a': 'No family member',
            'b': 'Grandparent, aunt, uncle, or first cousin',
            'c': 'Brother, sister, or own child',
            'd': 'Either parent',
            'e': 'Both parents',
        }.get(self.family_history, '')