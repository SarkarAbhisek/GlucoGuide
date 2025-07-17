from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import UserProfileForm, BloodTestForm, RiskAssessmentForm
from .models import UserProfile, BloodTest, RiskAssessment
from .risk_calculator import calculate_risk_scores

def home(request):
    return render(request, 'core/home.html')

def user_data(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if request.user.is_authenticated:
                profile.user = request.user
            profile.save()
            request.session['profile_id'] = profile.id
            if 'has_blood_test' in request.POST:
                return redirect('blood_test')
            return redirect('risk_assessment')
    else:
        form = UserProfileForm()
    return render(request, 'core/user_data.html', {'form': form})

def blood_test(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('user_data')
    
    if request.method == 'POST':
        form = BloodTestForm(request.POST)
        if form.is_valid():
            blood_test = form.save(commit=False)
            blood_test.user_profile = UserProfile.objects.get(id=profile_id)
            blood_test.save()
            return redirect('risk_assessment')
    else:
        form = BloodTestForm()
    return render(request, 'core/blood_test.html', {'form': form})

def risk_assessment(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('user_data')
    
    profile = UserProfile.objects.get(id=profile_id)
    
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            risk_assessment = form.save(commit=False)
            risk_assessment.user_profile = profile
            
            # Calculate BMI
            height = profile.height
            weight = profile.weight
            risk_assessment.bmi = weight / (height ** 2)
            
            # Calculate risk scores
            scores = calculate_risk_scores(profile, risk_assessment)
            risk_assessment.idrs_score = scores['idrs_score']
            risk_assessment.ada_score = scores['ada_score']
            risk_assessment.findrisc_score = scores['findrisc_score']
            
            risk_assessment.save()
            return redirect('results')
    else:
        form = RiskAssessmentForm()
    return render(request, 'core/risk_assessment.html', {'form': form, 'profile': profile})

def results(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('user_data')
    
    profile = UserProfile.objects.get(id=profile_id)
    try:
        blood_test = BloodTest.objects.filter(user_profile=profile).latest('created_at')
    except BloodTest.DoesNotExist:
        blood_test = None
    try:
        risk_assessment = RiskAssessment.objects.filter(user_profile=profile).latest('created_at')
    except RiskAssessment.DoesNotExist:
        risk_assessment = None
    
    return render(request, 'core/results.html', {
        'profile': profile,
        'blood_test': blood_test,
        'risk_assessment': risk_assessment,
    })

def generate_pdf(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('user_data')
    
    profile = UserProfile.objects.get(id=profile_id)
    try:
        blood_test = BloodTest.objects.filter(user_profile=profile).latest('created_at')
    except BloodTest.DoesNotExist:
        blood_test = None
    try:
        risk_assessment = RiskAssessment.objects.filter(user_profile=profile).latest('created_at')
    except RiskAssessment.DoesNotExist:
        risk_assessment = None
    
    template = get_template('core/prescription_pdf.html')
    context = {
        'profile': profile,
        'blood_test': blood_test,
        'risk_assessment': risk_assessment,
    }
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="glucoguide_prescription.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF')
    return response