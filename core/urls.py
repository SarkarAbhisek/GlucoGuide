from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-data/', views.user_data, name='user_data'),
    path('blood-test/', views.blood_test, name='blood_test'),
    path('risk-assessment/', views.risk_assessment, name='risk_assessment'),
    path('results/', views.results, name='results'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    #path('accounts/', include('django.contrib.auth.urls'))
]
