def calculate_risk_scores(profile, risk_assessment):
    try:
        age = profile.age
        gender = profile.gender
        height = profile.height
        weight = profile.weight
        waist = risk_assessment.waist
        physical_activity = risk_assessment.physical_activity
        family_history = risk_assessment.family_history
        hypertension = risk_assessment.hypertension
        high_blood_sugar_med = risk_assessment.high_blood_sugar_med
        fruit_intake = risk_assessment.fruit_intake
        high_blood_glucose = risk_assessment.high_blood_glucose
        
        # Calculate BMI with error handling
        try:
            bmi = weight / (height ** 2)
        except ZeroDivisionError:
            bmi = 0

        # Initialize scores with defaults
        scores = {
            'idrs_score': 0,
            'ada_score': 0,
            'findrisc_score': 0
        }

        # Age-based scores
        if age < 35:
            pass  # No score for young age
        elif 35 <= age <= 49:
            scores['idrs_score'] += 20
        elif age >= 50:
            scores['idrs_score'] += 30

        if 40 <= age <= 49:
            scores['ada_score'] += 1
        elif 50 <= age <= 59:
            scores['ada_score'] += 2
        elif age >= 60:
            scores['ada_score'] += 3

        if 45 <= age <= 54:
            scores['findrisc_score'] += 2
        elif 55 <= age <= 64:
            scores['findrisc_score'] += 3
        elif age >= 64:
            scores['findrisc_score'] += 4

        # Gender-based scores (for ADA)
        if gender == 'male':
            scores['ada_score'] += 1

        # Physical activity
        if physical_activity == 'c':
            scores['idrs_score'] += 30
            scores['findrisc_score'] += 2
        elif physical_activity == 'b':
            scores['idrs_score'] += 20

        # Family history
        if family_history == 'e':
            scores['idrs_score'] += 20
            scores['ada_score'] += 1
            scores['findrisc_score'] += 5
        elif family_history == 'd':
            scores['idrs_score'] += 10
            scores['ada_score'] += 1
            scores['findrisc_score'] += 5
        elif family_history == 'c':
            scores['findrisc_score'] += 5
        elif family_history == 'b':
            scores['findrisc_score'] += 3

        # Waist circumference
        if gender == 'female':
            if waist >= 90:
                scores['idrs_score'] += 20
            elif 80 <= waist < 90:
                scores['idrs_score'] += 10

            if waist > 88:
                scores['findrisc_score'] += 4
            elif 80 <= waist <= 88:
                scores['findrisc_score'] += 3
        elif gender == 'male':
            if waist >= 100:
                scores['idrs_score'] += 20
            elif 90 <= waist < 100:
                scores['idrs_score'] += 10

            if waist > 102:
                scores['findrisc_score'] += 4
            elif 94 <= waist <= 102:
                scores['findrisc_score'] += 3

        # Hypertension
        if hypertension:
            scores['ada_score'] += 1

        # High blood sugar medication
        if high_blood_sugar_med:
            scores['findrisc_score'] += 2

        # Fruit/vegetable intake
        if not fruit_intake:
            scores['findrisc_score'] += 1

        # High blood glucose
        if high_blood_glucose:
            scores['findrisc_score'] += 5

        # BMI-based scores
        if bmi > 40:
            scores['ada_score'] += 3
            scores['findrisc_score'] += 3
        elif bmi >= 30:
            scores['ada_score'] += 2
            scores['findrisc_score'] += 3
        elif bmi >= 25:
            scores['ada_score'] += 1
            scores['findrisc_score'] += 1

        return scores

    except Exception as e:
        # Return default scores in case of any error
        return {
            'idrs_score': 0,
            'ada_score': 0,
            'findrisc_score': 0
        }