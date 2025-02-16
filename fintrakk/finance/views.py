from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import requests
from .forms import UserRegistrationForm, TransactionForm, AccountForm, CategoryForm
from .models import Account, Category, Transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q
import io
import base64
import seaborn as sns
import csv
from django.http import HttpResponse
import openpyxl
import matplotlib
matplotlib.use('Agg')
from django.contrib.auth.models import User
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    return render(request, 'finance/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Checking if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Checking if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # Checking if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')

        # Createing user with hashed password
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'finance/register.html')

from django.db.models import Sum

@login_required
def dashboard(request):
    # Fetch all accounts and transactions for the logged-in user
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0

    # Count the total number of transactions
    total_transactions = transactions.count()

    return render(request, 'finance/dashboard.html', {
        'accounts': accounts,  # List of accounts with balances
        'transactions': transactions,
        'total_balance': total_balance,
        'total_transactions': total_transactions,
    })


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    # Adjust the account balance based on the transaction type
    account = transaction.account
    if transaction.type == 'Income':
        account.balance -= transaction.amount
    elif transaction.type == 'Expense':
        account.balance += transaction.amount
    account.save()

    # Delete the transaction
    transaction.delete()

    return HttpResponseRedirect(reverse('dashboard'))

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    account = transaction.account  

    # Store the original values before the transaction is modified
    original_amount = transaction.amount
    original_type = transaction.type

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            # Reverse the effects of the original transaction
            if original_type == 'Income':
                account.balance -= original_amount
            elif original_type == 'Expense':
                account.balance += original_amount

            # Save the updated transaction
            updated_transaction = form.save()

            # Apply the new transaction values
            if updated_transaction.type == 'Income':
                account.balance += updated_transaction.amount
            elif updated_transaction.type == 'Expense':
                account.balance -= updated_transaction.amount

            # Save the updated account balance
            account.save()

            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'finance/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            # Default to today's date if no date is provided
            if not transaction.date:
                transaction.date = date.today()

            transaction.save()

            # Update account balance
            account = transaction.account
            if transaction.type == 'Income':
                account.balance += transaction.amount
            elif transaction.type == 'Expense':
                account.balance -= transaction.amount
            account.save()

            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'finance/add_transaction.html', {'form': form})

@login_required
def manage_accounts(request):
    accounts = Account.objects.filter(user=request.user)  # Fetch all accounts for the user

    # Adding a new account
    if request.method == 'POST' and 'add_account' in request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_accounts')

    # Form for adding accounts
    form = AccountForm()

    return render(request, 'finance/manage_accounts.html', {
        'accounts': accounts,
        'form': form,
    })

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm(instance=account)

    return render(request, 'finance/edit_account.html', {'form': form, 'account': account})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    account.delete()
    return redirect('manage_accounts')

@login_required
def manage_categories(request):
    categories = Category.objects.filter(user=request.user)  # Fetch all user-specific categories

    # Adding a new category
    if request.method == 'POST' and 'add_category' in request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('manage_categories')

    # Form for adding categories
    form = CategoryForm()

    return render(request, 'finance/manage_categories.html', {
        'categories': categories,
        'form': form,
    })

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'finance/edit_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    return redirect('manage_categories')



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'finance/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

from django.db.models import Sum

@login_required
def get_report(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Multi-select filters
    selected_accounts = request.GET.getlist('account')
    selected_categories = request.GET.getlist('category')
    selected_types = request.GET.getlist('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    chart_type = request.GET.get('chart_type', 'bar')  # Default to bar chart

    # Apply filters
    if selected_accounts:
        transactions = transactions.filter(account_id__in=selected_accounts)
    if selected_categories:
        transactions = transactions.filter(category_id__in=selected_categories)
    if selected_types:
        transactions = transactions.filter(type__in=selected_types)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Convert queryset to Pandas DataFrame
    data = pd.DataFrame.from_records(transactions.values('date', 'category__name', 'type', 'amount'))

    if not data.empty:
        data['amount'] = pd.to_numeric(data['amount'], errors='coerce')
        data = data.dropna(subset=['amount'])

    # Generate the chart if data exists
    chart_url = generate_chart(data, chart_type) if not data.empty else None

    return render(request, 'finance/get_report.html', {
        'accounts': Account.objects.filter(user=request.user),
        'categories': Category.objects.filter(user=request.user),
        'chart_url': chart_url,
        'selected_accounts': selected_accounts,
        'selected_categories': selected_categories,
        'selected_types': selected_types,
    })

# Function to save chart to base64 URL for rendering in template
def save_chart_to_url():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

# Function to generate enhanced visualizations
def generate_chart(data, chart_type):
    if data.empty or 'amount' not in data.columns:
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, "No Data Available", fontsize=14, ha='center')
        return save_chart_to_url()

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")  # Improved aesthetics

    if chart_type == 'bar':
        grouped_data = data.groupby(['category__name'])['amount'].sum().sort_values(ascending=False)
        sns.barplot(x=grouped_data.values, y=grouped_data.index, hue=grouped_data.index, legend=False, palette="Blues_d")
        plt.xlabel("Total Amount")
        plt.ylabel("Category")
        plt.title("Spending by Category")

    elif chart_type == 'pie':
        grouped_data = data.groupby(['category__name'])['amount'].sum()
        plt.pie(
            grouped_data,
            labels=grouped_data.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette('pastel')
        )
        plt.legend(title="Categories", loc="best", bbox_to_anchor=(1, 1))
        plt.title("Expense Distribution")

    elif chart_type == 'line':
        grouped_data = data.groupby(['date'])['amount'].sum()
        sns.lineplot(x=grouped_data.index, y=grouped_data.values, marker='o', linestyle='-', color='blue')
        plt.xlabel("Date")
        plt.ylabel("Total Amount")
        plt.title("Expense/Income Trend Over Time")

    return save_chart_to_url()


@login_required
def download_chart(request, chart_type):
    transactions = Transaction.objects.filter(user=request.user)

    if not transactions.exists():
        return HttpResponse("No transactions available", status=400)

    # Convert transactions to DataFrame
    data = pd.DataFrame.from_records(transactions.values('date', 'category__name', 'type', 'amount'))

    # Convert 'amount' to numeric
    if not data.empty:
        data['amount'] = pd.to_numeric(data['amount'], errors='coerce')  # Convert to float
        data = data.dropna(subset=['amount'])  # Remove invalid rows

    # Ensure we have valid data
    if data.empty or 'amount' not in data.columns:
        return HttpResponse("No valid numeric data available to plot.", status=400)

    # Generate the requested chart
    generate_chart(data, chart_type)

    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png", bbox_inches='tight')
    plt.close()
    response["Content-Disposition"] = f"attachment; filename={chart_type}_chart.png"

    return response

from django.core.paginator import Paginator
@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Multi-select filters
    selected_accounts = request.GET.getlist('account')
    selected_categories = request.GET.getlist('category')
    selected_types = request.GET.getlist('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply filters
    if selected_accounts:
        transactions = transactions.filter(account_id__in=selected_accounts)
    if selected_categories:
        transactions = transactions.filter(category_id__in=selected_categories)
    if selected_types:
        transactions = transactions.filter(type__in=selected_types)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Fetch accounts and categories for filtering
    accounts = Account.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    return render(request, 'finance/transactions.html', {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'selected_accounts': selected_accounts,
        'selected_categories': selected_categories,
        'selected_types': selected_types,
    })

    


@login_required
def download_transactions(request, file_format='csv'):
    # Fetch all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user)

    # Apply filters from the request
    account_id = request.GET.get('account')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if account_id and account_id.isdigit():
        transactions = transactions.filter(account_id=account_id)
    if category_id and category_id.isdigit():
        transactions = transactions.filter(category_id=category_id)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Handle CSV download
    if file_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Account', 'Category', 'Description', 'Type', 'Amount'])
        for transaction in transactions:
            writer.writerow([
                transaction.date,
                transaction.account.name,
                transaction.category.name,
                transaction.description,
                transaction.type,
                transaction.amount
            ])
        return response

    # Handle Excel download
    elif file_format == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Transactions'

        # Write headers
        headers = ['Date', 'Account', 'Category', 'Description', 'Type', 'Amount']
        sheet.append(headers)

        # Write data
        for transaction in transactions:
            sheet.append([
                transaction.date,
                transaction.account.name,
                transaction.category.name,
                transaction.description,
                transaction.type,
                transaction.amount
            ])

        # Save workbook to the response
        workbook.save(response)
        return response

    return HttpResponse(status=400)  # Bad Request for unsupported formats


API_KEY = '1c8e8aba6ed93cd206149d4e'  
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

@login_required
def currency_conversion(request):
    response = requests.get(BASE_URL)
    data = response.json()

    if data['result'] == 'success':
        rates = data['conversion_rates']
    else:
        rates = {}
    amount = float(request.GET.get('amount', 0))
    from_currency = request.GET.get('from_currency', 'USD')
    to_currency = request.GET.get('to_currency', 'EUR')

    converted_amount = None
    if amount and from_currency in rates and to_currency in rates:
        usd_amount = amount / rates[from_currency]  # Convert to USD first
        converted_amount = usd_amount * rates[to_currency]  # Convert from USD to target currency

    return render(request, 'finance/currency_conversion.html', {
        'rates': rates,
        'converted_amount': converted_amount,
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
    })