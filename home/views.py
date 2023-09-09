from django.shortcuts import render , HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.
def index(request):
    allPosts=Post.objects.all()[:4]
    context={'allPosts':allPosts}
    return render(request,'home/index.html',context)
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        desc=request.POST['desc']
        if  len(name)<2 or len(email)<5 or len(desc)<3 or len(phone)<10:
            messages.error(request,"enter correct cradential")
        else:
            contact=Contact(name=name,email=email,phone=phone,desc=desc)
            contact.save()
            messages.success(request,"Contact Form is Submited")
    return render(request,'home/contact.html')




def about(request):
    return render(request,'home/about.html')

def search(request):
    query=request.GET['query']
    allPostTitle=Post.objects.filter(title__icontains=query)
    allPostContent=Post.objects.filter(content__icontains=query)
    allPosts=allPostTitle.union(allPostContent)
    params={'allPosts':allPosts,"query":query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method=="POST":

        # get the post parameters
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check inpot
        if len(username)>10:
            messages.error(request,"username should be under 10 charecter")
            return redirect('/')
        if not username.isalnum():
            messages.error(request,"username should be charecter and number")
            return redirect('/')
        if pass1!=pass2:
            messages.error(request,"Password did't match")
            return redirect('/')


        # create user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"created account in iCoder successfully!")
        return redirect("/")
    else:
        return HttpResponse("404 Not Found")

def handleLogin(request):
    if request.method=="POST": 
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully Looged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials, Please Try Again ")
            return redirect("/")
    return HttpResponse('404 Not Found')
def handleLogout(request):
    logout(request)
    messages.success(request,'logged Out Done')
    return redirect('/')