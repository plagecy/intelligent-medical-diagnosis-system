from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import SymptomForm
from .models import Prediction
from .symptoms import SYMPTOMS
import joblib
import pickle
import os

MODEL = joblib.load(os.path.join(settings.BASE_DIR, 'disease_model.pkl'))
ENCODER = joblib.load(os.path.join(settings.BASE_DIR, 'label_encoder.pkl'))




@login_required(login_url='login')
def home(request):
    form = SymptomForm()
    result = None

    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            input_data = [
                1 if form.cleaned_data.get(symptom) else 0
                for symptom in SYMPTOMS
            ]

            encoded_result = MODEL.predict([input_data])[0]
            result = ENCODER.inverse_transform([encoded_result])[0]

            Prediction.objects.create(
                user=request.user,
                symptoms=str(form.cleaned_data),
                result=result
            )

    return render(request, 'diagnosis/index.html', {
        'form': form,
        'result': result
    })





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'diagnosis/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'diagnosis/login.html')


def signup_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'diagnosis/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

