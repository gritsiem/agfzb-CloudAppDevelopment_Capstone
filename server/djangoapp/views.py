from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, DealerReview
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
dealers = get_dealers_from_cf()

# Create your views here.

# Create an `about` view to render a static about page
# def about(request):
# ...

def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):

def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    
    if request.method == "POST":
        fn = request.POST['fname']
        ln = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))

        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, password=password, first_name=fn, last_name=ln)
            login(request,user)
            # redirect to index
            return redirect("djangoapp:index")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = dealers
        # Concat all dealer's short name
        context["dealerships"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    if request.method == "GET":
        dealer_reviews = get_dealer_reviews_from_cf(dealer_id)  
        context["dealer"] = next((x.full_name for x in dealers if x.id == dealer_id), None)
        context["dealer_reviews"]=dealer_reviews
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method=="POST":
            review = dict()
            review["id"] = DealerReview.count+1
            DealerReview.count = DealerReview.count+1
            review["name"] = request.POST['name']
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase"] = True if 'purchasecheck' in request.POST else False 
            review["purchase_date"] = request.POST['purchasedate']
            car = CarModel.objects.get(id = request.POST["car"])
            # print(type(car.year))
            review["car_make"],review["car_model"], review["car_year"] = car.name,car.make.name,car.year.strftime("%Y")
            stamp = datetime.utcnow().isoformat()
            review["time"] = stamp
            json_payload=dict()
            json_payload["review"] = review
            url = 'https://9d9156f8.eu-gb.apigw.appdomain.cloud/api/review'
            response = post_request(url, json_payload)
            print(response)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        if request.method == "GET":
            name = next((x for x in dealers if x.id == dealer_id), None)
            cars = CarModel.objects.filter(dealerId=dealer_id)
            return render(request,"djangoapp/add_review.html", context = {"dealer_id" : dealer_id, 'dealer':name, 'cars': cars})
