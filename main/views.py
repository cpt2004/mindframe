from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import BlogPost


@never_cache
def index(request):

    posts = BlogPost.objects.all()
    
    return render(request,'main/index.html',{'posts': posts})

@never_cache
def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            password = request.POST['password']
            repeat_password = request.POST['repeat_password']
            email = request.POST['email']

            userlist = User.objects.values_list('username',flat=True)
            emaillist = User.objects.values_list('email',flat=True)

            if password != repeat_password:
                message = "Passwords do not match !!"
                return render(request,'main/signup.html',{'message': message})
            
            elif username in userlist:
                message = "Username already exists !!"
                return render(request,'main/signup.html',{'message': message})
            
            elif email in emaillist:
                error_message = "Email already exists !!"
                return render(request,'main/signup.html',{'message': message})
            
            else:
                try:
                    user = User.objects.create_user(username,email,password,first_name = firstname,last_name = lastname)
                    user.save()
                    login(request, user)
                    return redirect('/')
                
                except:
                    message = "Unexpected error occured !!"
                    return render(request,'main/signup.html',{'message':message})
        
        return render(request,'main/signup.html')
    return redirect('/')

@never_cache
def user_login(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            
            else:
                message = "Invalid Username or Password !!"
                return render(request,'main/login.html',{'message':message})
            
        return render(request,'main/login.html')
    
    return redirect('/')

def user_logout(request):
    logout(request)
    return redirect('/')

@never_cache
def delete_user(request):

    user = request.user

    try:
        user.delete()
        logout(request)
        message = "User deleted successfully !!"
        return redirect('/')
    
    except:
        message = "Couldn't delete user !!"
        return redirect('/')

@never_cache
def new_post(request):

    if request.method == 'POST':
        try:
            topic = request.POST['topic']
            content = request.POST['blog_content']

            blog_post = BlogPost(
                user = request.user,
                topic = topic,
                content = content,            
                )
            
            blog_post.save()

            message = "Blog post created successfully !!"
            return redirect('/')
        
        except:
            message = "Couldn't create blog post !!"
            return redirect('/')
        
    return render(request,'main/new_post.html')

def delete_post(request,post_id):

    posts = BlogPost.objects.all()
    post = get_object_or_404(BlogPost, id = post_id)
    if request.user == post.user:
        try:
            post.delete()
            message = "Blog post deleted successfully !!"
            return redirect('/')
        
        except:
            message = "Unexpected error occured !!"
            return redirect('/')
    
    message = "You don't have permission to make this action !!"
    return redirect('/')

def edit_post(request,post_id):

    
    posts = BlogPost.objects.all()
    post = get_object_or_404(BlogPost,id = post_id)
    
    if request.method == 'POST':
        try:
            post.topic = request.POST['topic']
            post.content = request.POST['blog_content']
            
            post.save()
            message = "Post Edited Successfully !!"
            return redirect('/',{'error_message':message, 'posts': posts})
        except:
            message = "Failed to Edit Post !!"
            return redirect('/',{'error_message':message, 'posts': posts})
    if request.user == post.user:
        return render(request,'main/edit_post.html',{'post':post})
    
    message = "You don't have permission to make this action !!"
    return redirect('/')

def error404(request):
    return render(request,'404.html')