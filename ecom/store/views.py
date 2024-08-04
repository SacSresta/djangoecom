from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import  messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def category(request, foo):
    # Check if a hyphen exists in the original string
    if '-' in foo:
        # Replacing hyphens with spaces if a hyphen is found
        foo_original = foo
        foo = foo.replace('-', ' ')
    else:
        foo_original = foo

    # Debugging: print the category name being searched for
    print(f"Original category string: {foo_original}")
    print(f"Processed category string: {foo}")
    
    try:
        # Look up the category
        category = Category.objects.get(name__iexact=foo)
        print(f"Category found: {category.name}")  # Debugging: print the category found
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        print(f"Category '{foo}' does not exist")  # Debugging: print the error message
        messages.error(request, f"The category '{foo_original}' does not exist")
        return redirect('home')
    
    
def product(request,pk):
    product = Product.objects.get(id = pk)
    return render(request,'product.html',{'product':product})

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})


def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in "))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            #log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have registered successfully"))
            return redirect('home')
        else:
            messages.success(request,("You have not registered successfully"))
            return redirect('register')
    else:    
        return render(request, 'register.html', {'form':form})