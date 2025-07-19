def generate_recommendations(profile, risk_assessment, blood_test):
    recommendations = {
        'urgent': [],
        'medical': [],
        'lifestyle': [],
        'diet': [],
        'exercise': [],
        'monitoring': []
    }

    # Urgent recommendations (high risk)
    if (risk_assessment and (
        (risk_assessment.idrs_score is not None and risk_assessment.idrs_score >= 60) or 
        (risk_assessment.findrisc_score is not None and risk_assessment.findrisc_score >= 15) or
        (blood_test and (
            (blood_test.fasting_glucose is not None and blood_test.fasting_glucose >= 126) or
            (blood_test.post_prandial_glucose is not None and blood_test.post_prandial_glucose >= 200) or
            (blood_test.hba1c is not None and blood_test.hba1c >= 6.5)
        )))):
        recommendations['urgent'].append(
            "Consult with a healthcare provider immediately as your results indicate "
            "a high risk of diabetes. You may need diagnostic testing."
        )

    # Medical recommendations
    if risk_assessment and (
        (risk_assessment.idrs_score is not None and risk_assessment.idrs_score >= 30) or 
        (risk_assessment.findrisc_score is not None and risk_assessment.findrisc_score >= 12)):
        recommendations['medical'].append(
            "Schedule a checkup with your healthcare provider to discuss your diabetes risk."
        )
    
    if risk_assessment and risk_assessment.hypertension:
        recommendations['medical'].append(
            "Regular monitoring of blood pressure and consultation with a healthcare provider."
        )

    # Lifestyle recommendations
    if risk_assessment and risk_assessment.bmi is not None and risk_assessment.bmi >= 23:
        recommendations['lifestyle'].append(
            "Weight management through a balanced diet and regular exercise to reduce your BMI."
        )
    
    if risk_assessment and risk_assessment.physical_activity == 'c':  # Sedentary
        recommendations['lifestyle'].append(
            "Increase physical activity to at least 30 minutes per day, 5 days a week."
        )

    # Diet recommendations (always included)
    diet_advice = [
        "Follow a balanced diet with controlled portions.",
        "Choose whole grains over refined carbohydrates.",
        "Include plenty of non-starchy vegetables in your meals.",
        "Limit intake of sugary foods and beverages.",
        "Choose lean protein sources like fish, poultry, and legumes.",
        "Include healthy fats from nuts, seeds, and olive oil."
    ]
    recommendations['diet'].extend(diet_advice)

    # Exercise recommendations (always included)
    exercise_plan = [
        "Aim for at least 150 minutes of moderate-intensity aerobic activity per week.",
        "Include strength training exercises 2-3 times per week.",
        "Incorporate flexibility exercises like yoga or stretching.",
        "Reduce sedentary time - take short activity breaks every 30 minutes."
    ]
    
    if risk_assessment and risk_assessment.bmi is not None and risk_assessment.bmi >= 30:
        exercise_plan.append(
            "Consider low-impact exercises like swimming or cycling if you have joint concerns."
        )
    recommendations['exercise'].extend(exercise_plan)

    # Monitoring recommendations
    monitoring = [
        "Monitor your weight weekly if trying to lose weight.",
        "Keep a food and activity diary to track patterns."
    ]
    
    if blood_test and (
        (blood_test.fasting_glucose is not None and blood_test.fasting_glucose >= 100) or 
        (blood_test.post_prandial_glucose is not None and blood_test.post_prandial_glucose >= 140) or 
        (blood_test.hba1c is not None and blood_test.hba1c >= 5.7)):
        monitoring.append(
            "Regular monitoring of blood sugar levels as you may be at risk for prediabetes."
        )
    recommendations['monitoring'].extend(monitoring)

    return recommendations