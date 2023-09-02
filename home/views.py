from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    # allPosts = Post.objects.all()[0:4]
    allPosts = Post.objects.order_by('-views')[0:4]
    return render(request, "home/home.html", {'allPosts':allPosts})


def about(request):
    return render(request, "home/about.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)==0 or len(email)==0 or len(phone)==0 or len(content)==0:
            messages.error(request, "Please submit the form correctly...")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Form has been submitted successfully!")
    return render(request, "home/contact.html")


def search(request):
    query = request.GET['query']
    allPostsTitle = Post.objects.filter(title__icontains = query)
    allPostsHeading1 = Post.objects.filter(heading1__icontains = query)
    allPostsContent1 = Post.objects.filter(content1__icontains = query)
    allPostsAuthor = Post.objects.filter(author__icontains = query)
    title_heading1 = allPostsTitle.union(allPostsHeading1)
    title_heading1_content1 = title_heading1.union(allPostsContent1)
    allPosts = title_heading1_content1.union(allPostsAuthor)
    return render(request, 'home/search.html', {'allPosts': allPosts, 'query': query})


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['signupUsername']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Checks
        if len(username)<3 or len(username)>20:
            messages.error(request, "Username should be of 4-20 characters...")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers...")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Both the entered passwords didn't match...")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your ScribbleHub account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']
        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in to your ScribbleHub account!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials... Please try again...")
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Logged out of your ScribbleHub account successfully!")
    return redirect('home')
