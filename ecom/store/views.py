from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import  messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms



def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id = request.user.id)
        form = UserInfoForm(request.POST or None,instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your info has been updated")
            return redirect('home')
        return render(request,"update_info.html",{"form":form})
    else:
        messages.success(request, "You must be logged in",)
        return redirect('home.html',{})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form?
        if request.method == "POST":
            form = ChangePasswordForm(current_user,request.POST)
            #IS the form valid
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password has been Updated....... ")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password.html')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('login')

    return render(request, "update_password.html", {})
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance=current_user)
        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)
            messages.success(request,"User has been updated")
            return redirect('home')
        return render(request,"update_user.html",{"user_form":user_form})
    else:
        messages.success(request, "You myust be logged in",)
        return redirect('home.html',{})
    
def category_summary(request):
    categories = Category.objects.all()
    
    return render(request,'category_summary.html',{'categories': categories})
def category(request, foo):
    categories = Category.objects.all()
    print(categories)
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
        return render(request, 'category.html', {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        print(f"Category '{foo}' does not exist")  # Debugging: print the error message
        messages.error(request, f"The category '{foo_original}' does not exist")
        return redirect('home')
    
    
def product(request,pk):
    product = Product.objects.get(id = pk)
    return render(request,'product.html',{'product':product})

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'home.html',{'products':products,'categories': categories})


def about(request):
    return render(request,'about.html',{})

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
            messages.success(request,("User name created. Please fill up your information."))
            return redirect('update_info')
        else:
            messages.success(request,("You have not registered successfully"))
            return redirect('register')
    else:    
        return render(request, 'register.html', {'form':form})