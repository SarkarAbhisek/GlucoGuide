def calculate_risk_scores(profile, risk_assessment):
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
    bmi = weight / (height ** 2)

    # Initialize scores
    idrs_score = 0
    ada_score = 0
    findrisc_score = 0

    # Age-based scores
    if age < 35:
        idrs_score += 0
    elif 35 <= age <= 49:
        idrs_score += 20
    elif age >= 50:
        idrs_score += 30

    if age < 40:
        ada_score += 0
    elif 40 <= age <= 49:
        ada_score += 1
    elif 50 <= age <= 59:
        ada_score += 2
    elif age >= 60:
        ada_score += 3

    if age < 45:
        findrisc_score += 0
    elif 45 <= age <= 54:
        findrisc_score += 2
    elif 55 <= age <= 64:
        findrisc_score += 3
    elif age >= 64:
        findrisc_score += 4

    # Gender-based scores (for ADA)
    if gender == 'male':
        ada_score += 1

    # Physical activity
    if physical_activity == 'c':
        idrs_score += 30
        findrisc_score += 2
    elif physical_activity == 'b':
        idrs_score += 20

    # Family history
    if family_history == 'e':
        idrs_score += 20
        ada_score += 1
        findrisc_score += 5
    elif family_history == 'd':
        idrs_score += 10
        ada_score += 1
        findrisc_score += 5
    elif family_history == 'c':
        findrisc_score += 5
    elif family_history == 'b':
        findrisc_score += 3

    # Waist circumference
    if gender == 'female':
        if waist >= 90:
            idrs_score += 20
        elif 80 <= waist < 90:
            idrs_score += 10

        if waist > 88:
            findrisc_score += 4
        elif 80 <= waist <= 88:
            findrisc_score += 3
    elif gender == 'male':
        if waist >= 100:
            idrs_score += 20
        elif 90 <= waist < 100:
            idrs_score += 10

        if waist > 102:
            findrisc_score += 4
        elif 94 <= waist <= 102:
            findrisc_score += 3

    # Hypertension
    if hypertension:
        ada_score += 1

    # High blood sugar medication
    if high_blood_sugar_med:
        findrisc_score += 2

    # Fruit/vegetable intake
    if not fruit_intake:
        findrisc_score += 1

    # High blood glucose
    if high_blood_glucose:
        findrisc_score += 5

    # BMI-based scores
    if bmi > 40:
        ada_score += 3
        findrisc_score += 3
    elif bmi >= 30:
        ada_score += 2
        findrisc_score += 3
    elif bmi >= 25:
        ada_score += 1
        findrisc_score += 1

    return {
        'idrs_score': idrs_score,
        'ada_score': ada_score,
        'findrisc_score': findrisc_score,
    }