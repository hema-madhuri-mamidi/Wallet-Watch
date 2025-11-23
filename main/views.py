from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json
import calendar
from datetime import date

from django.db.models import Sum
from django.db.models.functions import TruncMonth



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password =request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request,"User already exists please choose anoter")
            return render(request, 'register.html' )
        else:
            user= User.objects.create(
            username=username)
            user.set_password(password)
            user.save()
            messages.success(request, "account created successfully!'")
            login(request,user)
            return redirect('home_views')
    return render(request, 'register.html' )

def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Login successful!")
            return redirect('home_views')  # redirect to home page after login
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, "login.html")

    # if GET request — show empty form
    
    return render(request, 'login.html' )
def logout_views(request):
    logout(request)
    return redirect("login")

@login_required
def home_views(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'home.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')

        # Create a new expense linked to the user
        Expense.objects.create(
            user=request.user,
            name=name,
            amount=amount,
            category=category,
            date=date
        )

        messages.success(request, "Expense added successfully!")
        return redirect('home_views')

    return render(request, 'add_expense.html')


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        expense.name = request.POST.get('name')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.save()

        messages.success(request, "Expense updated successfully!")
        return redirect('home_views')

    return render(request, 'edit_expense.html', {'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully!")
    return redirect('home_views')



def charts(request):

    user = request.user   # current logged-in user

    # 1. Category-wise totals
    category_qs = (
        Expense.objects
        .filter(user=user)                   # FILTER BY USER
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    categories = [item['category'] for item in category_qs]
    category_amounts = [float(item['total']) for item in category_qs]

    top3 = category_qs[:3]

    # 2. Monthly totals
    year = date.today().year
    monthly_qs = (
        Expense.objects
        .filter(user=user, date__year=year)  # FILTER BY USER
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    months = [calendar.month_name[i] for i in range(1, 13)]
    month_totals = {item['month'].month: float(item['total']) for item in monthly_qs}

    monthly_amounts = [month_totals.get(i, 0) for i in range(1, 13)]

    total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'categories_json': json.dumps(categories),
        'category_amounts_json': json.dumps(category_amounts),
        'months_json': json.dumps(months),
        'monthly_amounts_json': json.dumps(monthly_amounts),
        'top3': top3,
        'total_expenses': float(total_expenses),
    }

    return render(request, 'charts.html', context)


# def charts(request):

#     category_qs = Expense.objects.values('category').annotate(total=Sum('amount')).order_by('-total')
    
#     categories = [item['category'] for item in category_qs]
#     category_amounts = [float(item['total']) for item in category_qs]

#     top3 = category_qs[:3]

#     year = date.today().year

#     monthly_qs = (
#         Expense.objects.filter(date__year=year)
#         .annotate(month=TruncMonth('date'))
#         .values('month')
#         .annotate(total=Sum('amount'))
#         .order_by('month')
#     )

#     months = [calendar.month_name[i] for i in range(1, 13)]
#     month_totals = {item['month'].month: float(item['total']) for item in monthly_qs if item['month']}

#     monthly_amounts = [month_totals.get(i, 0) for i in range(1, 13)]

#     total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

#     context = {
#         'categories_json': json.dumps(categories),
#         'category_amounts_json': json.dumps(category_amounts),
#         'months_json': json.dumps(months),
#         'monthly_amounts_json': json.dumps(monthly_amounts),
#         'top3': top3,
#         'total_expenses': float(total_expenses),
#     }

#     return render(request, 'charts.html', context)