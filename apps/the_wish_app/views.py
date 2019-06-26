from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Wish, Like
from apps.log_reg_app.models import User
from datetime import datetime
import bcrypt

def show_dashboard(request):
    if 'user_id' not in request.session.keys():
        return redirect("/")
    user_id = request.session['user_id']
    first_name = User.objects.get(id=user_id).first_name
    wishes = Wish.objects.all().filter(user_id=user_id).exclude(granted=True)
    other_wishes = Wish.objects.all().exclude(granted=False)
    wishObjs = []
    other_wishObjs = []
    likes = []
    for wish in wishes:
        wishObjs.append({'item':wish.item,
        'date_added': wish.date_added.strftime('%b %d %Y'),
        'id': wish.id})
    for wish in other_wishes:
        other_wishObjs.append({'item': wish.item,
        'first_name': User.objects.get(id=wish.user_id).first_name,
        'date_added': wish.date_added.strftime('%b %d %Y'),
        'date_granted': wish.date_granted.strftime('%b %d %Y'),
        'likes': len(Like.objects.all().filter(wish_id=wish.id)),
        'user_id': wish.user_id,
        'id': wish.id})
    context = {'my_wishes': wishObjs, 'user_id': user_id, 'other_wishes': other_wishObjs, 'first_name': first_name}
    return render(request, 'the_wish_app/index.html', context)

def new_wish(request):
    if 'user_id' not in request.session.keys():
        return redirect("/")
    user_id = request.session['user_id']
    first_name = User.objects.get(id=user_id).first_name
    context = { 'user_id': user_id, 'first_name': first_name}
    return render(request, 'the_wish_app/new_wish.html', context)

def wish_edit(request, wish_id):
    if 'user_id' not in request.session.keys():
        return redirect("/")
    user_id = request.session['user_id']
    wish = Wish.objects.get(id=wish_id)
    description = wish.description
    item = wish.item
    context = { 'wish_id': wish_id, 'description': description, 'item': item}
    return render(request, "the_wish_app/edit_wish.html", context)

def edit_wish(request, wish_id):
    if request.method == "POST":
        user_id = Wish.objects.get(id=wish_id).user_id
        user_id = int(user_id)
        item = request.POST['item']
        description = request.POST['description']
        user_id = Wish.objects.get(id=wish_id)
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                context = {'messages': messages}
            return redirect(f"/wishes/edit/{wish_id}", context)
        else:
            wish = Wish.objects.get(id=wish_id)
            wish.description = description
            wish.item = item
            wish.save()
            return redirect("/wishes")
    if request.method == "GET":
        return redirect("/")

def add_wish(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        item = request.POST['item']
        description = request.POST['description']
        date_added = datetime.now()
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                context = {'messages': messages}
            return redirect("/wishes/new", context)
        else:
            wish = Wish.objects.create(user_id=user_id, description=description, item=item, date_added=date_added)
            return redirect("/wishes")
    if request.method == "GET":
        return redirect("/")

def remove_wish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.delete()
    return redirect("/wishes")

def grant_wish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.granted = True
    wish.date_granted = datetime.now()
    wish.save()
    return redirect("/wishes")

def wish_stats(request):
    if 'user_id' not in request.session.keys():
        return redirect("/")
    user_id = request.session['user_id']
    first_name = User.objects.get(id=user_id).first_name
    total = len(Wish.objects.all().exclude(granted=False))
    granted = len(Wish.objects.all().filter(granted=True, user_id=user_id))
    pending = len(Wish.objects.all().filter(granted=False, user_id=user_id))
    context = { 'user_id': user_id, 'first_name': first_name, 'total': total, 'my_wishes': granted, 'my_pendding': pending}
    return render(request, "the_wish_app/stats.html", context)

def like_wish(request, wish_id):
    if request.method == "POST":
        user_id = request.session['user_id']
        errors = Like.objects.like_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                context = {'messages': messages}
            return redirect("/wishes", context)
        else:
            like = Like.objects.create(user_id=user_id, wish_id=wish_id)
            return redirect("/wishes")
    if request.method == "GET":
        return redirect("/")

def log_out(request):
    request.session.clear()
    return redirect("/")
