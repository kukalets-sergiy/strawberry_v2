
import os
from datetime import datetime
import datetime
from pathlib import Path

from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils.decorators import method_decorator
from strawberry_app.decorator import *
from strawberry_app.forms import RegistrationForm
from strawberry_app.serializers import *
from strawberry_app.models import *
from django_strawberry.urls import *
# from strawberry_app.filters import *

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponse
import requests
from PIL import Image
import calendar
from django.shortcuts import render
from django.utils import timezone
from calendar import Calendar, monthrange, month_name
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from .forms import PlantImageForm
from django.http import JsonResponse
from .forms import PlantImageForm




class CultureAPI(APIView):
    def get(self, request, culture_id=None):
        if culture_id is not None:
            try:
                culture = Culture.objects.get(id=culture_id)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CultureSerializer(culture)
            return Response(serializer.data, status=status.HTTP_200_OK)

        cultures = Culture.objects.all()
        serializer = CultureSerializer(cultures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        serializer = CultureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @method_decorator(unauthenticated_user)
    def put(self, request, culture_id):
        try:
            culture = Culture.objects.get(id=culture_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CultureSerializer(culture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @method_decorator(unauthenticated_user)
    def delete(self, request, culture_id):
        try:
            culture = Culture.objects.get(id=culture_id)
        except ObjectDoesNotExist:
            return Response({"message: culture doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        culture.delete()
        return Response({"message: culture was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class MonthsAPI(APIView):
    def get(self, request, months_id=None):
        if months_id is not None:
            try:
                month = Months.objects.get(id=months_id)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = MonthsSerializer(month)
            return Response(serializer.data, status=status.HTTP_200_OK)

        months = Months.objects.all()
        serializer = MonthsSerializer(months, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        serializer = MonthsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @method_decorator(unauthenticated_user)
    def put(self, request, months_id):
        try:
            month = Months.objects.get(id=months_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MonthsSerializer(month, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @method_decorator(unauthenticated_user)
    def delete(self, request, months_id):
        try:
            month = Months.objects.get(id=months_id)
        except ObjectDoesNotExist:
            return Response({"message: month doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        month.delete()
        return Response({"message: month was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


def register_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    return render(request, template_name='logout.html')


def homepage(request):
    return render(request, 'homepage.html')


def profile(request):
    return render(request, 'profile.html')


def search(request):
    query = request.GET.get('q')
    if query:
        cultures = Culture.objects.filter(
            Q(culture__icontains=query)
        )

        months = Months.objects.filter(
            Q(month__icontains=query) | Q(description__icontains=query) | Q(culture__culture__icontains=query)
        )
    else:
        cultures = Culture.objects.all()
        months = Months.objects.all()
    serializer_cultures = CultureSerializer(cultures, many=True)
    serializer_months = MonthsSerializer(months, many=True)
    context = {
        'cultures': serializer_cultures.data,
        'months': serializer_months.data,
        'search_query': query
    }
    if not cultures.exists() and not months.exists():
        context['error'] = 'Enter a valid search query'
    return render(request, 'search.html', context)


def create_cultures():
    strawberry = Culture.objects.create(name='Strawberry')
    tomatoes = Culture.objects.create(name='Tomatoes')
    potatoes = Culture.objects.create(name='Potatoes')

    for month in Months.objects.all():
        month.culture.add(strawberry, tomatoes, potatoes)


def all_objects_list(request):
    cultures = Culture.objects.all()
    months = Months.objects.all()

    context = {
        'cultures': cultures,
        'months': months,

    }
    return render(request, 'all_objects_list.html', context)


def culture_list(request):
    cultures = Culture.objects.all()
    context = {
        'cultures': cultures,
    }
    return render(request, 'culture_list.html', context)


def month_list(request):
    query = request.GET.get('q')
    if query:
        months = Culture.objects.filter(
            Q(month__icontains=query) | Q(culture__icontains=query) | Q(description__icontains=query)
        )
    else:
        months = Months.objects.all()
    serializer = MonthsSerializer(months, many=True)
    context = {
        'months': serializer.data,
        'search_query': query
    }
    return render(request, 'month_list.html', context)


def year_calendar(request, year=timezone.now().year):
    cal = []
    current_month = timezone.now().month
    for month in list(range(current_month, 13)) + list(range(1, current_month)):

        days = []
        for day in Calendar().itermonthdates(year, month):
            if day.month == month:
                days.append(day)
        cal.append({'month_name': month_name[month], 'days': days, 'num_days': len(days), 'month': month})
    return render(request, 'calendar.html', {'year': year, 'calendar': cal})


def month_detail(request, month, year, culture_id=None, month_id=None):
    if culture_id is not None:
        try:
            culture = Culture.objects.get(id=culture_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return render(request, 'month_detail.html', culture)

    if month_id is not None:
        try:
            month = Months.objects.get(id=culture_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return render(request, 'month_detail.html', month)

    cultures = Culture.objects.all()
    months = Months.objects.all()

    context = {
        'cultures': cultures,
        'months': months,

    }
    return render(request, 'month_detail.html', context)


def upload_images(request):
    if request.method == "POST":
        form = PlantImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("upload_images")
    else:
        form = PlantImageForm()
    plants = PlantImage.objects.all()
    return render(request=request, template_name="upload_images.html", context={'form': form, 'plants': plants})


def delete_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('upload_images')


def choose_month(request, month_id=None):
    if request.method == 'GET':
        strawberry = Culture.objects.first()  # Assuming there is only one strawberry object
        if strawberry:
            months = strawberry.months.all()
            selected_month_id = request.GET.get('month')
            selected_month = None
            if selected_month_id:
                try:
                    selected_month = months.get(id=selected_month_id)
                except ObjectDoesNotExist:
                    pass

            return render(request, 'choose_month.html', {'months': months, 'selected_month': selected_month})

    return redirect('choose_month')


def choose_culture(request, month_id=None):
    if request.method == 'GET':
        cultures = Culture.objects.all()
        selected_culture_id = request.GET.get('culture')
        selected_culture = None
        months = []

        if selected_culture_id:
            try:
                selected_culture = cultures.get(id=selected_culture_id)
                months = selected_culture.months.all()
            except ObjectDoesNotExist:
                pass

        return render(request, 'choose_culture.html', {'cultures': cultures, 'selected_culture': selected_culture,
                                                                                                      'months': months})

    return redirect('choose_culture')



def api_choose_culture(request, culture_id):
    if request.method == 'GET':
        try:
            culture = Culture.objects.get(id=culture_id)
            months = culture.months.all()
            month_data = [{'id': month.id, 'description': month.description} for month in months]
            return JsonResponse({'months': month_data})
        except ObjectDoesNotExist:
            return JsonResponse({'months': []})

