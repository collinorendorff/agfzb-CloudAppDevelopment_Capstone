from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        pw = request.POST['psw']
        user = authenticate(username=username, password=pw)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['notice'] = "Invalid username or password"
            return render(request, 'django/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        #taking in parameters and checking if this user already exists
        first = request.POST['firstname']
        last = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['psw']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist=True
        except:
            logger.error("New user detected")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first, last_name=last,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['notice'] = "This user already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://co2fc.us-east.cf.appdomain.cloud/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://co2fc.us-east.cf.appdomain.cloud/reviews/get-review"
        reviews = get_dealer_reviews_from_cf(url)
        context['dealer_id'] = dealer_id
        context['dealer'] = get_dealer_info(dealer_id)
        context['reviews'] = filter(lambda i: i.dealership == dealer_id, reviews)
    return render(request, 'djangoapp/dealer_details.html', context)

# helper function for get_dealer_details
def get_dealer_info(dealer_id):
    url = "https://co2fc.us-east.cf.appdomain.cloud/dealerships/dealer-get"
    alldealers = get_dealers_from_cf(url)
    return next(filter(lambda i: i.id == dealer_id, alldealers))

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        context['cars'] = CarModel.objects.all()
        context['dealer_id'] = dealer_id
        context['dealer'] = get_dealer_info(dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        url = "https://co2fc.us-east.cf.appdomain.cloud/api/review-post"
        jsonpayload = {}
        jsonpayload['name'] = request.POST['username']
        jsonpayload['dealership'] = dealer_id
        jsonpayload['review'] = request.POST['review']
        jsonpayload['purchase'] = request.POST['purchase']
        jsonpayload['purchase_date'] = request.POST['purchase_date']
        car = CarModel.objects.get(id = request.POST['car'])
        if car:
            jsonpayload['car_make'] = car.carmake.name
            jsonpayload['car_model'] = car.name
            jsonpayload['car_year'] = car.caryear.strftime("%Y")
        store_review(url, jsonpayload)
    return redirect('djangoapp:dealer_details', dealer_id = dealer_id)
