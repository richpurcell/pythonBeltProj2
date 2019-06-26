from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
# from apps.trip_buddy_app.models import Trip
from datetime import datetime
import bcrypt

def show_login(request):
    if request.method == "GET":
        print("*"*25 + "show_login" + "*"*25)
        print("In: show_login -> rendering index.html")
        return render(request, 'log_reg_app/index.html')

def process_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        errors = User.objects.login_validator(request.POST)
        context = { 'email': email, 'password': password }
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/", context)
        else:
            # There could be multiple instances of the desired email address
            users = User.objects.filter(email=email) # .password
            for user in users:
                passwd = user.password
                if bcrypt.checkpw(request.POST['password'].encode(), passwd.encode()):
                    request.session['user_id'] = user.id
                    return redirect("/success")
            try:
                del request.session['user_id']
            except KeyError:
                pass
            return redirect("/", context)

def process_registration(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        email = request.POST['email']
        birthday = request.POST['birthday']
        password = request.POST['password']
        errors = User.objects.registration_validator(request.POST)
        context = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'birthday': birthday}
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/", context)
        else:
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1, birthday=birthday )
            request.session['user_id'] = user.id
            return redirect("/success", context)

# def show_dashboard(request):
    if request.method == "GET":
        print("$"*60)
        user_id = request.session['user_id']
        if not request.session['user_id']: # every route that renders a page needs this!
            return redirect("/")
        first_name = User.objects.get(id=user_id).first_name
        # users = User.objects.all()
        trips = Trip.objects.all()
        this_user  = User.objects.get(id=user_id)
        my_trips = trips.filter(user_id=user_id)
        my_joined_trips = this_user.trips.all()
        other_trips = trips.exclude(user_id=user_id)
        tripObjs = []
        otherTripObjs =[]
        for trip in my_trips:
            tripObjs.append({
                'trip_id': trip.id,
                'user_id': trip.user_id, 
                'destination': trip.destination, 
                'start_date': trip.start_date.strftime('%Y-%m-%d'),
                'end_date': trip.end_date.strftime('%Y-%m-%d'), 
                'plan': trip.plan})
        for trip in my_joined_trips:
            tripObjs.append({
                'trip_id': trip.id,
                'user_id': trip.user_id,
                'destination': trip.destination,
                'start_date': trip.start_date.strftime('%Y-%m-%d'),
                'end_date': trip.end_date.strftime('%Y-%m-%d'),
                'plan': trip.plan})
        for trip in other_trips:
            otherTripObjs.append({
                'trip_id': trip.id,
                'user_id': trip.user_id,
                'destination': trip.destination,
                'start_date': trip.start_date.strftime('%Y-%m-%d'),
                'end_date': trip.end_date.strftime('%Y-%m-%d'),
                'plan': trip.plan})
        context = {'my_trips': tripObjs, 'other_trips':otherTripObjs, 'user_id': user_id, 'first_name': first_name}
        return render(request, 'the_wish_app/index.html', context)

def show_success(request):
    try:
        user_id = request.session['user_id']
    except KeyError:
        return redirect("/")
    user = User.objects.get(id=user_id)
    first_name = user.first_name
    # context = {'first_name': first_name, 'last_name': user.last_name, 'user_id': user.id } # ****COMMENT THIS OUT*****
    return redirect('/wishes') # ****************UNCOMMENT AND FIX THIS TO REDIRECT TO NEW APP****************
    # return render(request, 'log_reg_app/success.html', context) # ****COMMENT THIS OUT*****

def log_out(request):
    request.session.clear()
    return redirect("/")
