from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
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
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from django.http import HttpResponse

def home(request):
    return render(request, 'finance/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'finance/register.html', {'form': form})

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
def transactions(request):
    # Fetch all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Fetch accounts and categories for the logged-in user
    accounts = Account.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    # Filtering logic
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

    return render(request, 'finance/transactions.html', {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
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

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

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
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    # Fetch filtering options
    accounts = Account.objects.filter(user=user)
    categories = Category.objects.filter(user=user)

    # Retrieve filters from GET request
    account_id = request.GET.get('account')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    chart_type = request.GET.get('chart_type', 'bar')  # Default: bar chart

    # Apply filters
    if account_id:
        transactions = transactions.filter(account_id=account_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Convert queryset to Pandas DataFrame
    data = pd.DataFrame.from_records(transactions.values('date', 'category__name', 'type', 'amount'))

    # Convert 'amount' column to numeric (force errors to NaN and drop them)
    if not data.empty:
        data['amount'] = pd.to_numeric(data['amount'], errors='coerce')  # Convert to numeric
        data = data.dropna(subset=['amount'])  # Drop rows with NaN in 'amount'

    chart_url = generate_chart(data, chart_type) if not data.empty else None

    return render(request, 'finance/get_report.html', {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'chart_url': chart_url,
    })

def generate_chart(data, chart_type):
    if data.empty or 'amount' not in data.columns:
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, "No Data Available", fontsize=14, ha='center')
        return save_chart_to_url()

    plt.figure(figsize=(8, 5))

    if chart_type == 'bar':
        grouped_data = data.groupby(['category__name'])['amount'].sum()
        if grouped_data.empty:
            plt.text(0.5, 0.5, "No Data Available", fontsize=14, ha='center')
        else:
            grouped_data.plot(kind='bar', color='skyblue')
            plt.xlabel("Category")
            plt.ylabel("Total Amount")
            plt.title("Spending by Category")

    elif chart_type == 'pie':
        grouped_data = data.groupby(['category__name'])['amount'].sum()
        if grouped_data.empty:
            plt.text(0.5, 0.5, "No Data Available", fontsize=14, ha='center')
        else:
            plt.pie(
                grouped_data,
                labels=grouped_data.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=plt.cm.Paired.colors
            )
            plt.legend(title="Categories", loc="best", bbox_to_anchor=(1, 1))
            plt.title("Expense Distribution")

    elif chart_type == 'line':
        grouped_data = data.groupby(['date'])['amount'].sum()
        if grouped_data.empty:
            plt.text(0.5, 0.5, "No Data Available", fontsize=14, ha='center')
        else:
            grouped_data.plot(kind='line', marker='o', linestyle='-', color='blue')
            plt.xlabel("Date")
            plt.ylabel("Total Amount")
            plt.title("Expense/Income Trend Over Time")

    return save_chart_to_url()


def save_chart_to_url():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # Prevent overlapping elements
    buf.seek(0)
    plt.close()

    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

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

def transactions(request):
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(transactions_list, 10)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    accounts = Account.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    return render(request, 'finance/transactions.html', {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
    })


import csv
from django.http import HttpResponse
import openpyxl

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


import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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