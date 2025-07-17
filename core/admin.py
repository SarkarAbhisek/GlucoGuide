from django.contrib import admin
from .models import UserProfile, BloodTest, RiskAssessment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'height', 'weight')

@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'fasting_glucose', 'post_prandial_glucose', 'hba1c', 'random_glucose', 'created_at')

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'bmi', 'idrs_score', 'ada_score', 'findrisc_score', 'created_at')
