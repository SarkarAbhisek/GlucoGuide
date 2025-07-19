from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import UserProfileForm, BloodTestForm, RiskAssessmentForm
from .models import UserProfile, BloodTest, RiskAssessment
from .risk_calculator import calculate_risk_scores
from .recommendation_engine import generate_recommendations
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'core/home.html')

def user_data(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                if request.user.is_authenticated:
                    try:
                        existing_profile = UserProfile.objects.get(user=request.user)
                        existing_profile.name = profile.name
                        existing_profile.age = profile.age
                        existing_profile.gender = profile.gender
                        existing_profile.height = profile.height
                        existing_profile.weight = profile.weight
                        existing_profile.save()
                        profile = existing_profile
                    except UserProfile.DoesNotExist:
                        profile.user = request.user
                        profile.save()
                else:
                    profile.save()
                
                request.session['profile_id'] = profile.id
                if request.POST.get('has_blood_test') == 'on':
                    return redirect('blood_test')
                return redirect('risk_assessment')
            except Exception as e:
                # Log error here in production
                pass
    else:
        form = UserProfileForm()
    return render(request, 'core/user_data.html', {'form': form})

def blood_test(request):
    try:
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('user_data')
            
        profile = UserProfile.objects.get(id=profile_id)
    except (KeyError, ObjectDoesNotExist) as e:
        return redirect('user_data')
    
    if request.method == 'POST':
        form = BloodTestForm(request.POST)
        if form.is_valid():
            try:
                blood_test = form.save(commit=False)
                blood_test.user_profile = profile
                blood_test.save()
                return redirect('risk_assessment')
            except Exception as e:
                # Log error here in production
                pass
    else:
        form = BloodTestForm()
    return render(request, 'core/blood_test.html', {'form': form})

def risk_assessment(request):
    try:
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('user_data')
            
        profile = UserProfile.objects.get(id=profile_id)
    except (KeyError, ObjectDoesNotExist) as e:
        return redirect('user_data')
    
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            try:
                risk_assessment = form.save(commit=False)
                risk_assessment.user_profile = profile
                
                # Calculate BMI
                if profile.height and profile.weight:
                    try:
                        risk_assessment.bmi = profile.weight / (profile.height ** 2)
                    except ZeroDivisionError:
                        risk_assessment.bmi = None
                
                # Calculate risk scores
                scores = calculate_risk_scores(profile, risk_assessment)
                risk_assessment.idrs_score = scores.get('idrs_score', 0)
                risk_assessment.ada_score = scores.get('ada_score', 0)
                risk_assessment.findrisc_score = scores.get('findrisc_score', 0)
                
                risk_assessment.save()
                return redirect('results')
            except Exception as e:
                # Log error here in production
                pass
    else:
        form = RiskAssessmentForm()
    return render(request, 'core/risk_assessment.html', {'form': form, 'profile': profile})

def results(request):
    try:
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('user_data')
            
        profile = UserProfile.objects.get(id=profile_id)
        blood_test = BloodTest.objects.filter(user_profile=profile).order_by('-created_at').first()
        risk_assessment = RiskAssessment.objects.filter(user_profile=profile).order_by('-created_at').first()
        
        if not risk_assessment:
            return redirect('risk_assessment')
            
        recommendations = generate_recommendations(profile, risk_assessment, blood_test)
        
        context = {
            'profile': profile,
            'blood_test': blood_test,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations,
        }
        return render(request, 'core/results.html', context)
    except Exception as e:
        return redirect('user_data')

def generate_pdf(request):
    try:
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('user_data')
            
        profile = UserProfile.objects.get(id=profile_id)
        blood_test = BloodTest.objects.filter(user_profile=profile).order_by('-created_at').first()
        risk_assessment = RiskAssessment.objects.filter(user_profile=profile).order_by('-created_at').first()
        
        if not risk_assessment:
            return redirect('risk_assessment')
            
        recommendations = generate_recommendations(profile, risk_assessment, blood_test)
        
        template = get_template('core/prescription_pdf.html')
        context = {
            'profile': profile,
            'blood_test': blood_test,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations,
        }
        
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="glucoguide_prescription.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        if not pisa_status.err:
            return response
    except Exception as e:
        # Log error here in production
        pass
    
    return HttpResponse('We had some errors generating the PDF', status=500)